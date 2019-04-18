# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.forms.models import model_to_dict
from django.db.models import Q

from models import Event, encode_timestamp
from serializers import EventSerializer
import utils
from datetime import datetime


# 格式参考：http://timeline.knightlab.com/docs/json-format.html
def mk_timeline_event(i):
    e = dict(
                text=dict(
                    headline=i.abstract[:10]+(i.online_url and '<a href="%s" target="__blank">链接</a>'%i.online_url or ''),
                    text=i.abstract
                ),
                start_date=dict(year=i.year)
            )
    if i.year2 and i.year2-i.year>5:
        e['end_date'] = dict(year=i.year2)
    return e


@api_view(['GET'])
def search_event_index(request):
    q = Event.objects.order_by('year').filter(public_status__exact=True)
    if 'q' in request.GET:
        print request.GET['q']
        years, word = utils.parse_q(request.GET['q'])
        print years, word
        if years and isinstance(years, list):
            if len(years) > 0:
                q = q.filter(year__gte=years[0])
            if len(years) > 1:
                q = q.filter(year__lte=years[1])
        if word:
            q = q.filter(abstract__contains=word)
    timezones = []
    ids = []
    year1 = None
    year2 = None
    for i, event in enumerate(q):
        if not year1:
            year1 = event.year
        year2 = event.year
        ids.append(event.id)
        if len(ids) >= 100:
            if ids:
                timezones.append(dict(
                    id='%s-%s' % (year1, year2),
                    ids=ids,
                    title=('%s年~%s年' % (year1, year2)).replace('-', '前')
                ))
            ids = []
            year1 = year2
    if ids:
        timezones.append(dict(
            id='%s-%s' % (year1, year2),
            ids=ids,
            title=('%s年~%s年' % (year1, year2)).replace('-', '前')
        ))
    return Response(timezones)



@api_view(['GET'])
def get_timeline_search_events(request):
    page, size = 0, 10
    q = Event.objects.order_by('year').filter(public_status__exact=True)
    if 'p' in request.GET:
        page = int(request.GET['p'])
    if 'size' in request.GET:
        size = int(request.GET['size'])
    if 'q' in request.GET:
        print request.GET['q']
        years, word = utils.parse_q(request.GET['q'])
        print years, word
        if years and isinstance(years, list):
            if len(years) > 0:
                q = q.filter(year__gte=years[0])
            if len(years) > 1:
                q = q.filter(year__lte=years[1])
        if word:
            q = q.filter(abstract__contains=word)
    size = min(100, size)
    page = page * size
    size = page + size
    return Response(dict(
        events=map(mk_timeline_event, q[page:size])))


@api_view(['GET'])
def get_timeline_events(request, ids):
    events = Event.objects.order_by('year').filter(public_status__exact=True, id__in=map(int, ids.split(',')))
    return Response(dict(
        events=map(mk_timeline_event, events)))


@api_view(['GET'])
def get_events_by_ids(request, ids):
    events = Event.objects.order_by('year').filter(public_status__exact=True, id__in=map(int, ids.split(',')))
    events = map(lambda x:x.as_dict(), events)
    print len(events)
    return Response(events)


@api_view(["GET"])
def search_events(request):
    start = int(request.query_params['start'])
    end = int(request.query_params['end'])

    q = Event.objects.order_by('timestamp', 'level').all()
    q = q.filter(public_status=True)
    q = q.filter(Q(timestamp__gte=start)|Q(timestamp2__gte=start))
    q = q.filter(Q(timestamp__lte=end)|Q(timestamp2__lte=end))

    if 'q' in request.query_params:
        qw = request.query_params['q']
        q = q.filter(abstract__contains=qw)

    page, size = 0, 100
    if 'page' in request.query_params:
        page = int(request.query_params['page'])
    if 'page_size' in request.query_params:
        size = int(request.query_params['page_size'])
    size = min(100, size)
    page = page * size
    size = page + size
    serializer = EventSerializer(q[page:size], many=True)
    return Response(serializer.data)


def parse_date(s):
    # year[/month[/day]]
    parts = s.split('/')
    return encode_timestamp(
        int(parts[0]),
        len(parts) > 1 and int(parts[1]) or 0,
        len(parts) > 2 and int(parts[2]) or 0,
    )


def parse_dates(s):
    # year[/month[/day]][,year2[/month2[/day2]]]
    dates = s.split(',')
    return (
        len(dates) > 0 and parse_date(dates[0]) or None,
        len(dates) > 1 and parse_date(dates[1]) or None
    )


class EventView(APIView):
    def get(self, request, format=None):
        date1, date2 = None, None
        if 'dates' in request.query_params:
            date1, date2 = parse_dates(request.query_params['dates'])
        word = None
        if 'q' in request.query_params:
            word = request.query_params['q']

        if not date1 and not word:
            raise APIException('date and q can`t both empty')

        page, size = 0, 10
        if 'page' in request.query_params:
            page = int(request.query_params['page'])
        if 'page_size' in request.query_params:
            size = int(request.query_params['page_size'])
        size = min(20, size)
        page = page*size
        size = page+size

        q = Event.objects.all()
        if date1:
            q = q.filter(timestamp__gte=date1)
        if date2:
            q = q.filter(timestamp__lte=date2)
        if word:
            q = q.filter(abstract__contains=word)
        serializer = EventSerializer(q[page:size], many=True)
        return Response(serializer.data)


