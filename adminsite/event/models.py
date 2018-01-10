# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import math


class Event(models.Model):
    """
    Event
    """
    year = models.IntegerField(help_text='year of start time,is negative when BC,-238 means 238 BC')
    month = models.IntegerField(help_text='month of start time,1~12')
    day = models.IntegerField(help_text='day of start time,1~31')
    title = models.CharField(max_length=128)
    abstract = models.CharField(max_length=256)
    timestamp = models.IntegerField(help_text='s*(year*10000+month*100+day),s is -1 means BC,20180103=2018 AD/01/13,-3390413=339 BC/04/13')
    year2 = models.IntegerField(help_text='year of end time if existed,is negative when BC,-238 means 238 BC', null=True)
    month2 = models.IntegerField(help_text='month of end time if existed,1~12', null=True)
    day2 = models.IntegerField(help_text='day of end time if existed,1~31', null=True)

    def prepare(self):
        self.timestamp = (self.year < 0 and -1 or 1) * (abs(self.year) * 10000 + self.month * 100 + self.day)
        return self

    def save(self):
        super(Event, self.prepare()).save()

