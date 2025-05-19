from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    sent_messages = relationship("Message", back_populates="sender", foreign_keys='Message.sender_id')
    received_messages = relationship("Message", back_populates="receiver", foreign_keys='Message.receiver_id')

    def to_dict(self):
        return {"id": self.id, "email": self.email}

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])
