from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from config import *

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'

    hash_value = Column(String(), primary_key=True)
    orignal_name = Column(String)
    hash_name = Column(String)
    category = Column(String)
    description = Column(String)
    upload_time = Column(TIMESTAMP)

engine = create_engine('sqlite:///%s' % DB_NAME, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
