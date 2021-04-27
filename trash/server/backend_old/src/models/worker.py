# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from . import Base

class GraphicCard(Base):
    __tablename__ = 'graphic_cards'
    __table_args__ = {'schema': 'worker'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('worker.graphic_cards_id_seq'::regclass)"))
    name = Column(String(64), nullable=False)
    benchmark_score = Column(SmallInteger, nullable=False)
    price_per_hour = Column(SmallInteger, nullable=False)
    memory = Column(SmallInteger, nullable=False)

class Worker(Base):
    __tablename__ = 'workers'
    __table_args__ = {'schema': 'worker'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('worker.workers_id_seq'::regclass)"))
    token = Column(String(64), nullable=False, unique=True)
    private_key = Column(String(64), nullable=False)
    id_graphic_cards = Column(ForeignKey('worker.graphic_cards.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))
    id_users = Column(ForeignKey('user.users.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))
    id_tasks = Column(ForeignKey('task.tasks.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'), unique=True)

    graphic_card = relationship('GraphicCard')
    task = relationship('Task', uselist=False)
    user = relationship('User')


class Log(Base):
    __tablename__ = 'logs'
    __table_args__ = {'schema': 'worker'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('worker.logs_id_seq'::regclass)"))
    time = Column(DateTime, nullable=False)
    text = Column(Text, nullable=False)
    level = Column(SmallInteger, nullable=False)
    type = Column(String(32), nullable=False)
    id_workers = Column(ForeignKey('worker.workers.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'))

    worker = relationship('Worker')


class Status(Base):
    __tablename__ = 'status'
    __table_args__ = {'schema': 'worker'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('worker.status_id_seq'::regclass)"))
    last_connection_time = Column(DateTime, nullable=False)
    last_ip = Column(String(45))
    id_workers = Column(ForeignKey('worker.workers.id', ondelete='SET NULL', onupdate='CASCADE', match='FULL'), unique=True)

    worker = relationship('Worker', uselist=False)
