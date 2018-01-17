# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.contrib import admin
from django import forms

from django.shortcuts import render, redirect
from django.conf.urls import url
import utils
import requests

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
    actions = ['unpublish_event', 'publish_event']

    def publish_event(self, request, queryset):
        rows_updated = queryset.update(public_status=True)
        self.message_user(request, '%s was/were changed' % rows_updated)
    publish_event.short_description = "Publish events"

    def unpublish_event(self, request, queryset):
        rows_updated = queryset.update(public_status=False)
        self.message_user(request, '%s was/were changed' % rows_updated)
    unpublish_event.short_description = "UnPublish events"

    def import_html(self, request):
        if 'url' in request.GET:
            url = request.GET['url']
            response = requests.get(url, headers={
                # https://stackoverflow.com/questions/23651947/python-requests-requests-exceptions-toomanyredirects-exceeded-30-redirects
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
            })
            response.encoding = 'utf-8'
            html_str = response.text
            lines = ['1 !-!-!-! %s !-!-!-! %s'%i for i in utils.html2lines(html_str)]
            # print '\r\n'.join(lines)
        else:
            url = ''
            lines = []
        return render(request, 'admin/event/import.html', dict(
            url=url,
            lines=u'\r\n'.join(lines)
        ))

    def submit_lines(self, request):
        lines = request.POST['lines']
        if lines:
            lines = lines.split('\r\n')
            ents = []
            for l in lines:
                public_status, year, text = l.split('!-!-!-!')
                ents.append(Event(
                    year=int(year),
                    abstract=text,
                    public_status=bool(public_status)
                ).prepare())
            Event.objects.bulk_create(ents)
        return redirect('/admin/event/event')

    def get_urls(self):
        urls = super(EventAdmin, self).get_urls()
        my_urls = [
            url(r'import_html',
                self.admin_site.admin_view(self.import_html)),
            url(r'submit_lines',
                self.admin_site.admin_view(self.submit_lines)),
        ]
        return my_urls + urls

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'abstract':
            formfield.widget = forms.Textarea(attrs=dict(cols=100, rows=3))
        return formfield

    def get_search_results(self, request, queryset, search_term):
        years = None
        word = search_term
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

