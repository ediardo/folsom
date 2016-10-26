from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HouseRecord(Base):
    __tablename__ = 'house_records'
    id = Column(String(36), primary_key=True)
    date_posted = Column(Date)
    price = Column(Integer)
    beds = Column(SmallInteger)
    baths = Column(Float)
    sqft_house = Column(SmallInteger)
    sqft_lot = Column(Integer)
    floors = Column(Float)
    condition = Column(SmallInteger)
