import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from .alchemy_models import Base

# db = sqlalchemy.create_engine('postgresql://zaur:wsad1221@localhost:5432/zaurdb')
# db = sqlalchemy.create_engine('postgresql+psycopg2://zaur:wsad1221@localhost:5432/zaurdb')


def setup_alchemy():
    #admin_string = 'postgresql+psycopg2://postgres:postgres@/postgres'
    admin_string = 'postgresql+psycopg2://zaur:wsad1221@localhost:5432/zaurdb_admin'
    engine = sqlalchemy.create_engine(admin_string)
    with engine.connect() as conn:
        conn.execute("commit")
        conn.execute("create database zaurdb2; grant all on database zaurdb2 to zaur;")


def setup_admin_db():
    #admin_string = 'postgresql+psycopg2://zaur:wsad1221@localhost:5432/zaurdb'
    admin_string = 'sqlite:///zaur_admin.db'
    engine = sqlalchemy.create_engine(admin_string)
    with engine.connect() as conn:
        Base.metadata.create_all(conn)



