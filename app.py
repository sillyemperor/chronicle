import sys
sys.path.append('virenv')


import sqlalchemy
from mako.template import Template

from bottle import route, run, template

@route('/event')
def event_list():
    return template('<b>Hello {{name}}</b>!', name='Joe')

run(host='localhost', port=8080)

