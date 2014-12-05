import json
import os
from datetime import datetime

from sqlalchemy import Column, func, create_engine
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import config


Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hashname = Column(String, nullable=False, unique=True)
    size = Column(Integer, nullable=False)
    cat = Column(String, nullable=False)
    description = Column(String)
    created = Column(DateTime, default=func.now(), nullable=False)
    lastmodified = Column(DateTime, 
            default=func.now(), onupdate=func.now(), nullable=False)
    
    def __init__(self, name, hashname, size, cat, desc):
        self.name = name
        self.hashname = hashname
        self.size = size
        self.cat = cat
        self.description = desc


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

