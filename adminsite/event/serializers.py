# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Event, Tag

class EventSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields  = ['year', 'month', 'day', 'year2', 'month2', 'day2', 'abstract', 'online_url', 'location']

    def get_location(self, obj):
        if obj.longitude and obj.latitude:
            return [obj.longitude, obj.latitude]
        return None

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'




