from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from config import *
from datetime import *
import json

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'

    hash_value = Column(String, primary_key=True)
    origin_name = Column(String)
    hash_name = Column(String)
    file_size = Column(Integer)
    category = Column(String)
    description = Column(String)
    upload_time = Column(TIMESTAMP)

    def __init__(self):
        self.upload_time = datetime.today()

engine = create_engine('sqlite:///%s' % DB_NAME, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class ItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return {
                'hash_value': obj.hash_value,
                'origin_name': obj.origin_name,
                'hash_name': obj.hash_name,
                'file_size': obj.file_size,
                'category': obj.category,
                'description': obj.description,
                'upload_time': obj.upload_time
            }
        if isinstance(obj, datetime):
            return str(obj)[0:19]
        return json.JSONEncoder.default(self, obj)
