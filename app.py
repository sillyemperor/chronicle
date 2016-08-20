from bottle import get,post, route, run, template, request, redirect, response
import view
import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
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
        q = request.cookies['event-q'].decode('utf-8')

    p = int(request.query.p or 0)
    ps = int(request.query.ps or 10)
    # count = session.query(func.count('*')).select_from(models.Event).scalar()
    query = session.query(models.Event)
    if q:
        query = query.filter(models.Event.title.like('%'+q+'%'))
    return view.render('index.html',
                       title='Event',
                       query = q,
                       prev_p = p>0 and p-1 or 0,
                       next_p = p+1,
                       events=query.order_by(models.Event.year)[p*ps:p*ps+ps]
                       )


@get('/event')
def add_event():
    return view.render('event.html', title='Event', event=models.Event())


@post('/event')
def add_post_event():
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
    session.add(models.Event(
        title = unicode(title, 'utf-8'),
        abstract = unicode(abstract, 'utf-8'),
        year = year,
        month = month,
        day = day,
        year2 = year2,
        month2 = month2,
        day2 = day2,
        online_uri_list=online_uri_list,
        thumbnail_uri_list = thumbnail_uri_list
    ))
    session.commit()
    redirect('/event')


@get('/event/<id:int>')
def edit_event(id):
    return view.render('event.html', title='Event', event=session.query(models.Event).filter(models.Event.id == id).one())


@post('/event/<id:int>')
def edit_post_event(id):
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

    event = session.query(models.Event).filter(models.Event.id == id).one()
    event.abstract = unicode(abstract, 'utf-8')
    event.title = unicode(title, 'utf-8')
    event.year = year
    event.month = month
    event.day = day
    session.commit()

    redirect('/')

run(host='localhost', port=8080)

