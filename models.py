from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import *

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, doc='year,is negative when BC')
    month = Column(Integer, nullable=False, doc='month')
    day = Column(Integer, nullable=False, doc='day')
    title = Column(String(64), nullable=False)
    abstract = Column(String(512), nullable=True)
    online_uri_list = Column(String(2048), nullable=True, doc='use comma to separate uris.')
    thumbnail_uri_list = Column(String(2048), nullable=True, doc='use comma to separate uris.')
    year2 = Column(Integer, doc='year,is negative when BC')
    month2 = Column(Integer, doc='month')
    day2 = Column(Integer, doc='day')

