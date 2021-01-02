# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text, text
from sqlalchemy.orm import relationship

from . import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'user'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"user\".users_id_seq'::regclass)"))
    login = Column(String(32), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    register_date = Column(DateTime, nullable=False)


class Log(Base):
    __tablename__ = 'logs'
    __table_args__ = {'schema': 'user'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"user\".logs_id_seq'::regclass)"))
    time = Column(DateTime, nullable=False)
    text = Column(Text, nullable=False)
    id_users = Column(ForeignKey('user.users.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))

    user = relationship('User')


class Notification(Base):
    __tablename__ = 'notifications'
    __table_args__ = {'schema': 'user'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"user\".notifications_id_seq'::regclass)"))
    text = Column(Text, nullable=False)
    level = Column(SmallInteger, nullable=False)
    time = Column(DateTime, nullable=False)
    id_users = Column(ForeignKey('user.users.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))

    user = relationship('User')


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'user'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"user\".roles_id_seq'::regclass)"))
    role = Column(String(64), nullable=False, unique=True)
    id_users = Column(ForeignKey('user.users.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))

    user = relationship('User')


class Session(Base):
    __tablename__ = 'sessions'
    __table_args__ = {'schema': 'user'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"user\".sessions_id_seq'::regclass)"))
    login_time = Column(DateTime, nullable=False)
    last_activity_time = Column(DateTime, nullable=False)
    ip = Column(String(45), nullable=False)
    id_users = Column(ForeignKey('user.users.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))

    user = relationship('User')
