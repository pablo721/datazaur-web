
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd

# db = sqlalchemy.create_engine('postgresql://zaur:wsad1221@localhost:5432/zaurdb')
# db = sqlalchemy.create_engine('postgresql+psycopg2://zaur:wsad1221@localhost:5432/zaurdb')
# postgres://username:password@host:port/database_name


def get_connection_string(dialect, driver, username, password, host, port, database_name):
    # print(dialect, driver, username, password, host, port, database_name)
    return dialect + '+' + driver + '://' + username + ':' + password + '@' + host + ':' + port + '/' + database_name




def column_list_to_string(col_list):
    return str(col_list).replace("'", '')[1:-1]





