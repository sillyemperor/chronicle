# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Event

def event_date_info(e):
    return '%s~%s'%(e.year, e.year2)
event_date_info.short_description = 'date'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('year', 'title', 'abstract')
    search_fields = ['title', 'abstract']

