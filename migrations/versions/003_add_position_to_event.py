from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    event = Table('event', meta, autoload=True)
    Column('x', Float).create(event)
    Column('y', Float).create(event)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    event = Table('event', meta, autoload=True)
    event.c.x.drop()
    event.c.y.drop()
