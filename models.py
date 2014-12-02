import json
import os

from sqlalchemy import Column, func, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import config


Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hashname = Column(String, unique=True)
    size = Column(Integer)
    cat = Column(String)
    description = Column(String)
    created = Column(DateTime, default=func.now())
    lastmodified = Column(DateTime, 
            default=func.now(), onupdate=func.now())


class ItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return {
                'id': obj.id,
                'name': obj.name,
                'hashname': obj.hashname,
                'size': obj.size,
                'cat': obj.cat,
                'description': obj.description,
                'created': obj.created,
                'lastmodified': obj.lastmodified
            }
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)
        
engine = create_engine('sqlite:///%s' % config.DB_NAME, echo=config.DEBUG)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

