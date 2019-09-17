import asyncio
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, BigInteger
from sqlalchemy.orm import relationship
from db import Base

from sqlalchemy import event
from config import manager_client as client

subscriptions = Table('subscriptions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('channel_id', String, ForeignKey('channels.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    language_code = Column(String)
    channels = relationship("Channel",
                    secondary=subscriptions,
                    backref="subs")


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(String, primary_key=True)
    title = Column(String)
    username = Column(String)
    link = Column(String)
    last_id = Column(Integer)



@event.listens_for(Channel, 'after_insert')
def receive_after_insert(mapper, connection, target):
    print("Priviet ya callback", flush=True)
    asyncio.create_task(client.send_message(258273164, "Привет, я колбэк C:"))