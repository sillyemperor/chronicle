import json
import os,os.path

import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import settings
engine = create_engine(settings.test_db, echo=True)
Session = sessionmaker(engine)
session = Session()

for i in os.listdir('./dist/cache'):
    with open('./dist/cache/'+i, 'r') as f:
        s = f.read()
        o = json.loads(s)
        if 'timeline' not in o:
            continue
        for e in o['timeline']['date']:
            ymd = e['startDate'].split(',')
            evnt = models.Event(title=e['headline'], abstract=e['text'], year=ymd[0], month=ymd[1], day=ymd[2])
            session.add(evnt)
        session.commit()



