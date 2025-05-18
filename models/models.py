from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(Integer)

    def to_dict(self):
        return {"name": self.name, "age": self.age}
