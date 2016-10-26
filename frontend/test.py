from models.house_record import HouseRecord
from models.user import User
from models.result import Result
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime
import uuid
import hashlib

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///house_record.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

#users
users = ['admin', 'user', 'anna', 'jake']
try:
    for u in users:
        pwd_hash = hashlib.sha256("secret_pass_" + u).hexdigest()
        user = User(username=u, password=pwd_hash)
        session.add(user)
    session.commit()
except IntegrityError:
    #users alrady in db, recreating session
    session = Session()

#records
my_csv = open('kc_house_data.csv', 'r')
i = 0
record_ids = []
for line in my_csv.readlines():
    values = line.replace('"',"").split(',')[:11]
    if values[0] == 'id':
        continue
    h = HouseRecord()
    h.id = str(uuid.uuid4())
    h.user_id = i % len(users) + 1
    h.date_posted = datetime.datetime.strptime(values[1].split('T')[0],"%Y%m%d").date()
    h.price = values[2]
    h.beds = values[3]
    h.baths = values[4]
    h.sqft_house = values[5]
    h.sqft_lot = values[6]
    h.floors = values[7]
    h.condition = values[10]
    i += 1
    record_ids.append(h.id)
    session.add(h)
session.commit()

#results
res = ["a", "b", "c"]
i = 0
for r_id in record_ids:
    r = Result(id=r_id, result=res[i%len(res)])
    i += 1
    session.add(r)
session.commit()
