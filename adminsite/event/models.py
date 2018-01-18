# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import math


def encode_timestamp(year, month, day):
    return (year < 0 and -1 or 1) * (abs(year) * 10000 + month * 100 + day)

class Event(models.Model):
    """
    Event
    """
    year = models.IntegerField(help_text='year of start time,is negative when BC,-238 means 238 BC')
    month = models.IntegerField(help_text='month of start time,1~12', default=0)
    day = models.IntegerField(help_text='day of start time,1~31', default=0)
    title = models.CharField(max_length=128, blank=True, null=True)
    abstract = models.CharField(max_length=3000)
    timestamp = models.IntegerField(help_text='s*(year*10000+month*100+day),s is -1 means BC,20180103=2018 AD/01/13,-3390413=339 BC/04/13')
    year2 = models.IntegerField(help_text='year of end time if existed,is negative when BC,-238 means 238 BC', blank=True, null=True)
    month2 = models.IntegerField(help_text='month of end time if existed,1~12', blank=True, null=True)
    day2 = models.IntegerField(help_text='day of end time if existed,1~31', blank=True, null=True)
    online_url = models.URLField(help_text='Online resource html', max_length=3000, blank=True, null=True)
    public_status = models.BooleanField(help_text='Is public', default=False)
    CRUCIAL_EVENT = 1
    KEY_EVENT = 2
    NORMAL_EVENT = 3
    EVENT_LEVELS = (
        (CRUCIAL_EVENT, '极其重要的事件'),
        (KEY_EVENT, '关键的事件'),
        (NORMAL_EVENT, '过渡性事件'),
    )
    level = models.SmallIntegerField(max_length=2, choices=EVENT_LEVELS, default=NORMAL_EVENT)

    def prepare(self):
        self.timestamp = encode_timestamp(self.year, self.month, self.day)
        return self

    def save(self):
        super(Event, self.prepare()).save()

