# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from models import Event

def event_date_info(e):
    if not e.year2:
        return e.year
    delta = e.year2 - e.year
    if delta <=0:
        return e.year
    return '%s~%s(%s)'%(e.year, e.year2, delta)
event_date_info.short_description = 'years'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_per_page = 10
    fields = (('year', 'month', 'day'), 'abstract', ('year2', 'month2', 'day2'), 'online_url')
    exclude = ['timestamp']
    list_display = (event_date_info, 'abstract')
    search_fields = ['abstract', 'year']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'abstract':
            formfield.widget = forms.Textarea(attrs=dict(cols=100, rows=3))
        return formfield

