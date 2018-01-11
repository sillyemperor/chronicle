# -*- coding: utf-8 -*-
from fabric.api import run
from fabric.state import env

def host_type():
    run('uname -s')
