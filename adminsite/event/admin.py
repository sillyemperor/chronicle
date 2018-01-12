# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

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
    fields = (('year', 'month', 'day'), 'public_status', 'abstract', 'title', ('year2', 'month2', 'day2'), 'online_url')
    exclude = ['timestamp']
    list_display = (event_date_info, 'public_status', 'abstract', 'title')
    search_fields = ['abstract', 'year', 'title']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'abstract':
            formfield.widget = forms.Textarea(attrs=dict(cols=100, rows=3))
        return formfield

    def get_search_results(self, request, queryset, search_term):
        years = None
        word = None
        m = re.match(r'(?P<years>[-]?\d+[~][-]?\d+)([+]{1}(?P<word>.+))?', search_term)
        if m:
            groups = m.groupdict()
            if 'years' in groups:
                years = map(int, groups['years'].split('~'))
            if 'word' in groups:
                word = groups['word']
        queryset, use_distinct = super(EventAdmin, self).get_search_results(request, queryset, word)
        if years and len(years) == 2:
            queryset &= Event.objects.filter(year__gte=years[0]).filter(year__lte=years[1])
        return queryset, use_distinct

