from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    event = Table('event', meta, autoload=True)
    year2 = Column('year2', Integer)
    year2.create(event)
    month2 = Column('month2', Integer)
    month2.create(event)
    day2 = Column('day2', Integer)
    day2.create(event)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    event = Table('event', meta, autoload=True)
    event.c.year2.drop()
    event.c.month2.drop()
    event.c.day2.drop()
