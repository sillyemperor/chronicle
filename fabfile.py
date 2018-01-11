# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.state import env

env.project_root = 'chronicle/adminsite'

def venv():
    with cd('chronicle'):
        run('source venv/bin/activate')
        run('python -m pip install -r requirements.txt')

def deploy_static():
    with cd(env.project_root):
        run('python manage.py collectstatic -v0 --noinput')
        run('python manage.py migrate')
        run('pkill -9 gunicorn')
        run('gunicorn -c gunisettings.py adminsite.wsgi & > /dev/null')



