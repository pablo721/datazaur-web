import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from .alchemy_utils import get_connection_string, column_list_to_string

# db = sqlalchemy.create_engine('postgresql://zaur:wsad1221@localhost:5432/zaurdb')
# db = sqlalchemy.create_engine('postgresql+psycopg2://zaur:wsad1221@localhost:5432/zaurdb')
# postgres://username:password@host:port/database_name


def merge_from_temp(temp_table, dest_table):
    pass


def ingest_merge(df, table_name, columns, key_columns):
    passwd = os.environ.get("LOCAL_DB_PASS")
    # print(passwd)
    conn_string = get_connection_string('postgresql', 'psycopg2', 'zaur', 'wsad1221', 'localhost', '5432', 'zaurdb2')
    engine = sqlalchemy.create_engine(conn_string)
    temp_name = 'tmp_' + table_name
    df.to_sql(temp_name, engine, if_exists='replace', index=False)

    #engine.execute(query)


def load_data(src_table, dst_table, src_engine, dst_engine, mapping=None):
    try:
        df = pd.read_sql_table(src_table, src_engine, index_col=None)
        df.to_sql(dst_table, dst_engine, if_exists='append', index=False)
        return 0
    except Exception as e:
        return 1, e


conn_string = get_connection_string('postgresql', 'psycopg2', 'zaur', 'wsad1221', 'localhost', '5432', 'zaurdb2')
eng = sqlalchemy.create_engine(conn_string)
load_data('tmp_calendar__macrocalendar', 'calendar__macrocalendar', eng, eng)



######

def write_record(name, details, engine):
    engine.execute("INSERT INTO records (name,details) VALUES ('%s','%s')" % (name, details))

def read_record(field, name, engine):
    result = engine.execute("SELECT %s FROM records WHERE name = '%s'" % (field, name))
    return result.first()[0]

def update_record(field, name, new_value, engine):
    engine.execute("UPDATE records SET %s = '%s' WHERE name = '%s'" % (field, new_value, name))

def write_dataset(name, dataset, engine):
    dataset.to_sql('%s' % (name), engine, index=False, if_exists='replace', chunksize=1000)

def read_dataset(name, engine):
    try:
        dataset = pd.read_sql_table(name, engine)
    except:
        dataset = pd.DataFrame([])
    return dataset

def list_datasets(engine):
    datasets = engine.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
    return datasets.fetchall()