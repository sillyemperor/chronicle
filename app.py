from bottle import get,post, route, run, template, request, redirect, response
import view
import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_, and_
from sqlalchemy import func
import base64

import settings
engine = create_engine(settings.db, echo=True)
Session = sessionmaker(engine)
session = Session()


@get('/')
def index():
    q = request.query.q
    if q:
        response.set_cookie('event-q', q.encode('utf-8'))
    if 'clear' in request.query:
        response.set_cookie('event-q', '')
        request.cookies['event-q'] = ''

    if 'q' not in request.query:
        q = 'event-q' in request.cookies and request.cookies['event-q'].decode('utf-8') or ''

    p = int(request.query.p or 0)
    ps = int(request.query.ps or 10)
    # count = session.query(func.count('*')).select_from(models.Event).scalar()
    query = session.query(models.Event)
    if q:
        if q[-2:] == 'AD' and q[:-2].isdigit():
            y = int(q[:-2])
            query = query.filter(models.Event.year==y)
        elif  q[-2:] == 'BC' and q[:-2].isdigit():
            y = -int(q[:-2])
            query = query.filter(models.Event.year==y)
        else:
            query = query.filter(or_(models.Event.title.like('%'+q+'%'), models.Event.abstract.like('%'+q+'%')))
    return view.render('index.html',
                       title='Event',
                       query = q,
                       prev_p = p>0 and p-1 or 0,
                       next_p = p+1,
                       events=query.order_by(models.Event.year, models.Event.month, models.Event.day)[p*ps:p*ps+ps]
                       )


@get('/event')
@get('/event/<id:int>')
def event(id=0):
    try:
        event = session.query(models.Event).filter(models.Event.id == id).one()
    except:
        event = models.Event()
    return view.render('event.html', title='Event', referer=request.headers.get('Referer'), event=event)

@get('/event/next/<id:int>')
def next_event(id=0):
    try:
        event = session.query(models.Event).filter(models.Event.id == id).one()
        event = session.query(models.Event).filter(models.Event.timestamp > event.timestamp)\
            .order_by(models.Event.timestamp)\
            .first()
    except Exception as ext:
        return ext.message
    redirect('/event/%d' % event.id)

@get('/event/last/<id:int>')
def last_event(id=0):
    try:
        event = session.query(models.Event).filter(models.Event.id == id).one()
        event = session.query(models.Event).filter(models.Event.timestamp < event.timestamp)\
            .order_by(models.Event.timestamp.desc())\
            .first()
    except Exception as ext:
        return ext.message
    redirect('/event/%d' % event.id)

@post('/event')
@post('/event/<id:int>')
def post_event(id=0):
    title = request.forms.get('title')
    abstract = request.forms.get('abstract')
    year = request.forms.get('year')
    month = request.forms.get('month')
    day = request.forms.get('day')
    year2 = request.forms.get('year2')
    month2 = request.forms.get('month2')
    day2 = request.forms.get('day2')
    online_uri_list = request.forms.get('online_uri_list')
    thumbnail_uri_list = request.forms.get('thumbnail_uri_list')
    x = request.forms.get('x')
    y = request.forms.get('y')
    timestamp = year*10000+month*100+day

    event = session.query(models.Event).filter(models.Event.id == id).one()

    try:
        if event:
            event.abstract = unicode(abstract, 'utf-8')
            event.title = unicode(title, 'utf-8')
            event.year = year
            event.month = month
            event.day = day
            event.year2 = year2
            event.month2 = month2
            event.day2 = day2
            event.online_uri_list = online_uri_list
            event.thumbnail_uri_list = thumbnail_uri_list
            event.x = x
            event.y = y
            event.timestamp = timestamp
        else:
            event = models.Event(
                title=unicode(title, 'utf-8'),
                abstract=unicode(abstract, 'utf-8'),
                year=year,
                month=month,
                day=day,
                year2=year2,
                month2=month2,
                day2=day2,
                online_uri_list=online_uri_list,
                thumbnail_uri_list=thumbnail_uri_list,
                x=x,
                y=y,
                timestamp=timestamp
            )
            session.add(event)
        session.commit()
    except:
        session.rollback()
    redirect('/event/%d' % event.id)

run(host='localhost', port=8080)

