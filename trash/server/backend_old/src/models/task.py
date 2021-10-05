# coding: utf-8
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        SmallInteger, String, Text, text)
from sqlalchemy.orm import relationship

from . import Base


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'task'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('task.tasks_id_seq'::regclass)"))
    file_path = Column(Text, nullable=False)
    id_users = Column(ForeignKey('user.users.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))

    user = relationship('User')


class CustomSetting(Base):
    __tablename__ = 'custom_settings'
    __table_args__ = {'schema': 'task'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('task.custom_settings_id_seq'::regclass)"))
    id_tasks = Column(ForeignKey('task.tasks.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'), unique=True)

    task = relationship('Task', uselist=False)


class Setting(Base):
    __tablename__ = 'settings'
    __table_args__ = {'schema': 'task'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('task.settings_id_seq'::regclass)"))
    id_tasks = Column(ForeignKey('task.tasks.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'), unique=True)

    task = relationship('Task', uselist=False)


class Status(Base):
    __tablename__ = 'status'
    __table_args__ = {'schema': 'task'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('task.status_id_seq'::regclass)"))
    finished = Column(Boolean, nullable=False)
    progress = Column(SmallInteger, nullable=False)
    id_tasks = Column(ForeignKey('task.tasks.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'), unique=True)

    task = relationship('Task', uselist=False)
