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
from database_handler import DatabaseHandler

handler = DatabaseHandler('sqlite:///house_record.db')
#handler = DatabaseHandler('sqlite:///:memory:')

#users
users = ['admin', 'user', 'anna', 'jake']
try:
    for u in users:
        pwd_hash = hashlib.sha256("secret_pass_" + u).hexdigest()
        handler.save_user(u, pwd_hash)
except IntegrityError:
    #users already in db, recreating session
    pass

#records
my_csv = open('kc_house_data.csv', 'r')
i = 0
records = []
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
    records.append(h)
    if i > 20:
        break

handler.save_records(records)
record_ids = [r.id for r in records]

#results
results = ["a", "b", "c"]
i = 0
for r_id in record_ids:
    handler.save_result(results[i%len(results)], r_id)

handler.get_data_for_user(users[0])
