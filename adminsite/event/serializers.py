# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields  = ['year', 'month', 'day', 'year2', 'month2', 'day2', 'abstract', 'online_url']




