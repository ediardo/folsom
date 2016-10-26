from models.house_record import HouseRecord
from models.user import User
from models.result import Result
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json


class DatabaseHandler():

    def __init__(self, connection_string):
        # self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.engine = create_engine('sqlite:///house_record.db', echo=False)
        Base.metadata.create_all(self.engine)
        self.make_session = sessionmaker(bind=self.engine)

    def save_records(self, records):
        session = self.make_session()
        session.add_all(records)
        session.commit()

    def get_user_id_by_login(self, login):
        print login
        session = self.make_session()
        id, = session.query(User.id).filter(User.username == login)
        return id[0]

    def get_data_for_user(self, login):
        user_id = self.get_user_id_by_login(login)
        session = self.make_session()

        results = session.query(HouseRecord).filter(HouseRecord.user_id == 1)
        return results

    def save_user(self, username, pwd_hash):
        session = self.make_session()
        user = User(username=username, password=pwd_hash)
        session.add(user)
        session.commit()

    def save_result(self, result, record_id, action="default"):
        session = self.make_session()
        r = Result(id=record_id, result=result, action=action)
        session.add(r)
        session.commit()