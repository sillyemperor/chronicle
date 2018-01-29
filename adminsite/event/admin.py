# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.contrib import admin
from django import forms

from django.shortcuts import render, redirect
from django.conf.urls import url
import utils
import requests
import re
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers

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
    fields = (('year', 'month', 'day'), 'public_status', 'abstract', 'title',
              ('year2', 'month2', 'day2'), 'level', 'online_url', ('longitude', 'latitude'))
    exclude = ['timestamp']
    list_display = (event_date_info, 'level', 'public_status', 'abstract', 'title')
    search_fields = ['abstract', 'year', 'title']
    actions = ['set_event_public_status_action', 'set_event_level_action']

    change_form_template = 'admin/event/change_form.html'

    def change_field(self, request, queryset, field):
        value = request.POST[field]
        for obj in queryset:
            self.log_change(request, obj, 'set %s=%s' % (field, value))
        rows_updated = queryset.update(**{field:value})
        self.message_user(request, '%s was/were changed' % rows_updated)

    def set_event_public_status_action(self, request, queryset):
        if request.POST.get('post'):
            self.change_field(request, queryset, 'public_status')
            return None
        return render(request, 'admin/event/set_public_status.html', dict(
            queryset=queryset,
            action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
            status=(
                (1, 'Publish'),
                (0, 'Hide')
            )
        ))
    set_event_public_status_action.short_description = "Change public status of events"

    def set_event_level_action(self, request, queryset):
        if request.POST.get('post'):
            self.change_field(request, queryset, 'level')
            return None
        return render(request, 'admin/event/set_level.html', dict(
            queryset=queryset,
            action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
            levels=Event.EVENT_LEVELS
        ))
    set_event_level_action.short_description = "Change level of events"

    def import_html(self, request):
        if 'url' in request.GET:
            url = request.GET['url']
            response = requests.get(url, headers={
                # https://stackoverflow.com/questions/23651947/python-requests-requests-exceptions-toomanyredirects-exceeded-30-redirects
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
            })
            s = response.content
            r = utils.matchstr(s, ('gb2312', 'utf-8', 'utf8'), False)
            if r:
                response.encoding = r[0]
            print response.encoding
            # html_str = response.text#response.text.encode(response.encoding).decode('utf-8')
            lines = ['1 !-!-!-!3 !-!-!-! %s !-!-!-! %s'%i for i in utils.html2lines(response.text)]
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
                public_status, level, year, text = l.split('!-!-!-!')
                ents.append(Event(
                    year=int(year),
                    abstract=text,
                    public_status=bool(public_status),
                    level=int(level),
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
        years, word = utils.parse_q(search_term)
        queryset, use_distinct = super(EventAdmin, self).get_search_results(request, queryset, word)
        if years and len(years) == 2:
            queryset &= Event.objects.filter(year__gte=years[0]).filter(year__lte=years[1])
        return queryset, use_distinct

