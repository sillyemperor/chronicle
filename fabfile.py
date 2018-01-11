# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.state import env
from fabvenv import virtualenv


def deploy():
    with cd('chronicle'):
        run('git pull')
        with virtualenv('venv/'):
            run('python -m pip install -r requirements.txt')
    with cd('chronicle/adminsite'):
        with virtualenv('../venv/'):
            run('python manage.py collectstatic -v0 --noinput')
            run('python manage.py migrate')
            run('supervisorctl restart chronic')



