from sqlalchemy import MetaData, Table, Column, Integer, String, select, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Config(Base):
    __tablename__ = 'config'
    key = Column(String(32), primary_key=True)
    value = Column(String(256), nullable=False)


class Update(Base):
    __tablename__ = 'update'
    table = Column(String(32), primary_key=True)
    updated = Column(DateTime, nullable=True)


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    source = Column(String(32))
    timestamp = Column(DateTime, nullable=True)
    message = Column(String(512), nullable=True)
    status = Column(Integer, nullable=True)


class Dataset(Base):
    __tablename__ = 'dataset'
    name = Column(String(128), primary_key=True)
    code = Column(String(64), nullable=True)
    source = Column(String(64), nullable=True)
    table_name = Column(String(64), nullable=True)
    refresh_rate = Column(Integer, nullable=True)
    last_updated = Column(Integer, nullable=True)
    description = Column(String(512), nullable=True)



class Source(Base):
    __tablename__ = 'source'
    name = Column(String(128), primary_key=True)
    url = Column(String(64), nullable=True)
    api_key = Column(String(256), nullable=True)


class Dataflow(Base):
    __tablename__ = 'dataflow'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))


class Pipeline(Base):
    __tablename__ = 'pipeline'
    name = Column(String(32), primary_key=True)









