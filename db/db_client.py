
from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os


class BaseDbClient:
    dialect = 'postgresql'
    driver = 'psycopg2'
    username = 'zaur'
    host = 'localhost'
    port = '5432'
    database = 'zaurdb2'


    def __init__(self, url):
        self.engine = create_engine(url)

    def create_schema(self, schema_name):
        try:
            self.engine.execute(f'create schema {schema_name};')
            self.engine.execute(f'grant all on schema {schema_name} to zaur;')
        except Exception as e:
            print(f'Exception: {e}')

    def connect_engine(self, database):
        password = os.environ.get('LOCAL_DB_PASS')
        url = self.get_db_url(self.dialect, self.driver, self.username, password, self.host, self.port, database)
        self.engine = create_engine(url)

    @staticmethod
    def get_db_url(dialect, driver, username, password, host, port, database, filepath=None):
        if dialect == 'sqlite':
            return dialect + ':////' + filepath
        return dialect + '+' + driver + '://' + username + ':' + password + '@' + host + ':' + port + '/' + database

    def get_secret(self, key):
        with open('./secrets.json') as file:
            return json.loads(file.read())[key]

    def save_df_to_db(self, df, table, schema='public', if_exists='replace'):
        Session = sessionmaker(self.engine)
        with Session() as session:
            try:
                df.to_sql(table, self.engine, schema, if_exists, index=False)
                session.commit()
                print(f'Session committed.')
            except Exception as e:
                print(f'Error: {e} \nRolling back session.')
                session.rollback()

