from models.house_record import HouseRecord
from models.house_record import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///house_record.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()
my_csv = open('kc_house_data.csv', 'r')

for line in my_csv.readlines():
    values = line.replace('"',"").split(',')[:11]
    if values[0] == 'id':
        continue
    h = HouseRecord()
    h.date_posted = datetime.datetime.strptime(values[1].split('T')[0],"%Y%m%d").date()
    h.price = values[2]
    h.beds = values[3]
    h.baths = values[4]
    h.sqft_house = values[5]
    h.sqft_lot = values[6]
    h.floors = values[7]
    h.condition = values[10]
    session.add(h)


# engine = create_engine('sqlite:///:memory:', echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind = engine)
# session = Session()
# hdate = datetime.datetime.strptime('20141118T00000'.split('T')[0], "%Y%m%d").date()
# h = HouseRecord(date_posted=hdate, floors=2, beds=1, baths=1.5)
# print(h)
# session.add(h)
#print(session.dirty)
session.commit()