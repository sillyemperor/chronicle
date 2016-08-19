from bottle import get,post, route, run, template, request, redirect
import view
import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import settings
engine = create_engine(settings.db, echo=True)
Session = sessionmaker(engine)
session = Session()

@get('/')
def index():
    return view.render('index.html',title='Event',events=session.query(models.Event).order_by(models.Event.year)[0:20])

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
        title = title,
        abstract = abstract,
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
    redirect('/')

@get('/event/<id:int>')
def get_event(id):
    return view.render('event.html', title='Event', event=session.query(models.Event).filter(models.Event.id == id).one())

@post('/event/<id:int>')
def post_event(id):
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

