from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HouseRecord(Base):
    __tablename__ = 'house_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_posted = Column(Date, primary_key=False)
    price = Column(Integer, primary_key=False)
    beds = Column(SmallInteger, primary_key=False)
    baths = Column(Float, primary_key=False)
    sqft_house = Column(SmallInteger, primary_key=False)
    sqft_lot = Column(Integer, primary_key=False)
    floors = Column(Float, primary_key=False)
    condition = Column(SmallInteger, primary_key=False)