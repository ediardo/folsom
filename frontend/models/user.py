from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(64), nullable=False)