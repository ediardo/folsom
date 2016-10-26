from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from base import Base


class Result(Base):
    __tablename__ = 'results'
    id = Column(String(36), ForeignKey("house_records.id"), primary_key=True)
    result = Column(String(50))
    action = Column(String(10))