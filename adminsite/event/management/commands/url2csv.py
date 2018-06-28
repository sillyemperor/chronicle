# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
import os, os.path
import csv
import requests
import event.utils


class Command(BaseCommand):
    help = 'Parse wiki text to csv file'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs=1, type=str, help='URL of page to parse')
        parser.add_argument('csvfile', nargs=1, type=str, help='Out file path')

    def handle(self, *args, **options):
        url = options['url'][0]
        csv_file = options['csvfile'][0]
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
        s = response.content
        r = event.utils.matchstr(s, ('gb2312', 'utf-8', 'utf8'), False)
        if r:
            response.encoding = r[0]
        lines = event.utils.html2lines(response.text)

        with open(csv_file, 'w+') as fp:
            writer = csv.writer(fp, delimiter=';'.encode('utf8'),
                                lineterminator=os.linesep,
                       quotechar='"'.encode('utf8'), quoting=csv.QUOTE_ALL)
            for l in lines:
                writer.writerow([
                    # public_status, level, abstract, year, [month, day, year2, month2, day2, longitude, latitude]
                    0, 3, l[0].encode('utf8'), l[1], '', '', l[2]
                ])

        self.stdout.write(self.style.SUCCESS('OK'))

