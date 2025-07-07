from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    mac = Column(String)
    imei = Column(String)
    device_id = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="devices", lazy="joined")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    devices = relationship("Device", back_populates="user", lazy="joined")
