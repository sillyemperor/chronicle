# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from models import Event, encode_timestamp
from serializers import EventSerializer


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
