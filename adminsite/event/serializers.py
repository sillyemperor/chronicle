# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Event, Tag

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields  = ['year', 'month', 'day', 'year2', 'month2', 'day2', 'abstract', 'online_url']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'




