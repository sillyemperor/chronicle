from sqlalchemy import *
from migrate import *

meta = MetaData()

event = Table(
    'event', meta,
    Column('id', Integer, primary_key=True),
    Column('year', Integer,nullable=file,doc='year,is negative when BC'),
    Column('month', Integer,nullable=file,doc='month'),
    Column('day', Integer,nullable=file,doc='day'),
    Column('title', String(64),nullable=file),
    Column('abstract', String(512),nullable=true),
    Column('online_uri_list', String(2048),nullable=true,doc='use comma to separate uris.'),
    Column('thumbnail_uri_list', String(2048),nullable=true,doc='use comma to separate uris.'),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    event.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    event.drop()
