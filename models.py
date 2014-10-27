from sqlalchemy import Column, String

class Item():
    __tablename__ = 'item'

    hash_value = Column(String, primary_key=True)
    orignal_name = Column(String)
    hash_name = Column(String)
    category = Column(String)
    description = Column(String)
    upload_time = Column(Date)

