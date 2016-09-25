from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    event = Table('event', meta, autoload=True)
    Column('timestamp', BigInteger, default=0).create(event)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    event = Table('event', meta, autoload=True)
    event.c.timestamp.drop()
