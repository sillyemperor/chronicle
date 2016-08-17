from bottle import get,post, route, run, template, request
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
    return view.render('index.html',title='Event',events=session.query(models.Event)[0:20])

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
    if event:
        event.title = title
    else:
        pass
    session.commit()






run(host='localhost', port=8080)

