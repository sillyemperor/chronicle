# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.state import env


def deploy():
    with cd('chronicle'):
        run('git pull')
        run('source venv/bin/activate')
        run('python -m pip install -r requirements.txt')
        with cd('adminsite'):
            run('python manage.py collectstatic -v0 --noinput')
            run('python manage.py migrate')
            run('pkill -9 gunicorn')
            run('gunicorn -c gunisettings.py adminsite.wsgi & > /dev/null')



