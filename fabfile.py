# -*- coding: utf-8 -*-
from fabric.api import run
from fabric.state import env

env.user = 'root'
env.password = 'Qwer3306Cd'

def host_type():
    run('uname -s')

def pull():
    run('git pull')