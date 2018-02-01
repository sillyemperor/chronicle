# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
import os, os.path
import csv
import re


class Command(BaseCommand):
    help = 'Parse wiki text to csv file'

    def add_arguments(self, parser):
        parser.add_argument('wikifiles', nargs=1, type=str, help='One file or dir of Wiki files')
        parser.add_argument('csvfile', nargs=1, type=str, help='Out file path')

    def handle(self, *args, **options):
        wiki_files = options['wikifiles'][0]
        csv_file = options['csvfile'][0]
        with open(csv_file, 'w+') as fp:
            writer = csv.writer(fp, delimiter=';'.encode('utf8'),
                                lineterminator=os.linesep,
                       quotechar='"'.encode('utf8'), quoting=csv.QUOTE_ALL)
            if os.path.isdir(wiki_files):
                self.do_dir(wiki_files, writer);
            else:
                self.do_file(wiki_files, writer);
        self.stdout.write(self.style.SUCCESS('OK'))

    def rebuild(self, s):
        return s.replace('*', '').replace('[', '').replace(']', '').strip()

    def do_record(self, s , tag):
        s = self.rebuild(s)
        if not s:
            return None
        m = re.match(r'(?P<month>\d+)[月](?P<day>\d+)?[日]?', s)
        month = None
        day = None
        if m:
            if m.groupdict().has_key('month') and m.group('month'):
                month = int(m.group('month'))
            if m.groupdict().has_key('day') and m.group('day'):
                day = int(m.group('day'))
        s = (tag in ('出生', '逝世') and tag + ':' or '') + s
        return s.encode('utf8'), month, day

    def do_file(self, file_path, writer):
        self.stdout.write(file_path)
        with open(file_path, 'r') as fp:
            year = None
            events = []
            tag = None
            for l in fp.readlines():
                s = l.decode('utf8')
                if s.startswith('*') and tag in ['大事记', '出生', '逝世']:
                    e = self.do_record(s, tag)
                    if e:
                        events.append(e)
                elif s.startswith('=='):
                    m = re.match(r'== (?P<tag>\W+) ==', s)
                    if m:
                        tag = m.group('tag')
                        print tag
                elif not year:
                    m = re.match(r'[[][[]Category:[前]?(?P<year>\d+)[年][|][*, \w][]][]]', s)
                    if m:
                        year = int(m.group('year'))
                        if '前' in s:
                            year = -year
                        print year
            if year:
                for e in events:
                    writer.writerow([
                        # public_status, level, abstract, year, [month, day, year2, month2, day2, longitude, latitude]
                        0, 3, e[0], year, e[1], e[2]
                    ])

    def do_dir(self, dir, writer):
        for i in os.listdir(dir):
            self.do_file(os.path.join(dir, i), writer)


