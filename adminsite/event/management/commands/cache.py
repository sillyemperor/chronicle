from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from event.models import Event

class Command(BaseCommand):
    help = 'Manipulate cache files'

    def add_arguments(self, parser):
        parser.add_argument('command', nargs=1, type=str)
        parser.add_argument('dir', nargs=1, type=str)

    def handle(self, *args, **options):
        if 'import' in options['command']:
            self.do_import(*args, **options)
        self.stdout.write(self.style.SUCCESS('OK'))

    def do_import(self, *args, **options):
        import os, os.path
        import json
        cache_dir = options['dir'][0]
        with open(os.path.join(cache_dir, 'info.json')) as fp:
            ents = []
            for i in json.load(fp):
                file = os.path.join(cache_dir, '%s.json'%i['id'])
                with open(file) as fp2:
                    for e in json.load(fp2)['timeline']['date']:
                        year, month, day = (int(i) for i in e['startDate'].split(','))
                        year2, month2, day2 = (int(i) for i in e['endDate'].split(','))
                        ents.append(Event(
                            year=year, month=month, day=day, year2=year2, month2=month2, day2=day,
                            title=e['text'], abstract=e['headline']
                        ).prepare())
                print(file)
            Event.objects.bulk_create(ents)



