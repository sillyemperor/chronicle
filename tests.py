import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import settings

engine = create_engine(settings.test_db, echo=True)

Session = sessionmaker(engine)
session = Session()

evnt = models.Event(title='test',year=-1000,month=1,day=1)
session.add(evnt)

session.commit()
