from django.utils.dateparse import parse_datetime
import investpy
import sqlalchemy
import datetime
import time
import pandas as pd
import json
import requests
import csv
import os
from sqlalchemy import create_engine
from .alchemy_utils import get_connection_string


alpha_key = '1WEDCC91HCX5F7U4'
finmodel_key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
username = 'zaur'
password = 'wsad1221'  # os.environ.get("LOCAL_DB_PASS")
conn_string = get_connection_string('postgresql', 'psycopg2', username, password, 'localhost', '5432', 'zaurdb2')
engine = sqlalchemy.create_engine(conn_string)


class CalendarLoader:

    def __init__(self, db_url):
        self.engine = create_engine(db_url)


    def load_macro_calendar(self):
        df = investpy.economic_calendar()
        print(df)
        #ingest_merge(calendar, 'calendar__macrocalendar', list(calendar.columns), ['id'])
        #calendar.to_sql('calendar__macrocalendar', engine, if_exists='replace', index=False)
        return df



    def load_ipo_calendar(self, start_date='2021-01-01', end_date='2022-12-31'):
        token = 'cbcepm2ad3ib4g5ukl2g'
        url = f"https://finnhub.io/api/v1/calendar/ipo?from={start_date}&to={end_date}&token={token}"
        df = pd.DataFrame(json.loads(requests.get(url).text)['ipoCalendar'])
        df['id'] = df.index
        #df.to_sql('calendar__ipocalendar', engine, if_exists='replace', index=False)
        return df


    def load_earnings_calendar(self):
        CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={alpha_key}'
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(my_list[1:], columns=my_list[0])
            df['id'] = df.index
            #df.to_sql('calendar__earningscalendar', engine, if_exists='replace', index=False)
            return df


    def load_crypto_calendar(self):
        url = "https://developers.coinmarketcal.com/v1/events"
        querystring = {"max": "100"}
        payload = ""
        headers = {
            'x-api-key': "8kn6nhe3Dw8bkt0NnQx5p52ImfmUwjcm8g9GMlO8",
            'Accept-Encoding': "deflate, gzip",
            'Accept': "application/json"
        }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        df = pd.DataFrame(json.loads(response.text)['body'])
        df['title'] = df['title'].apply(lambda x: x['en'])
        df['coins'] = df['coins'].apply(lambda x: str(list(pd.DataFrame(x)['id'])).replace('[', '').replace(']', '').replace("'", ""))
        df['categories'] = df['categories'].apply(lambda x: str(list(pd.DataFrame(x)['name'])).replace('[', '').replace(']', '').replace("'", ""))
        df['date_event'] = df['date_event'].apply(lambda x: pd.to_datetime(x))
        df['created_date'] = df['created_date'].apply(lambda x: pd.to_datetime(x))
        #df.to_sql('calendar__cryptocalendar', engine, if_exists='replace', index=False)
        return df


    def load_all_calendars(self):
        dfs = {}
        for func in [self.load_crypto_calendar, self.load_earnings_calendar, self.load_ipo_calendar, self.load_macro_calendar]:
            try:
                df = func()
                dfs[func.__name__.replace('load_', '')] = df
            except Exception as e:
                print(f'Exception: {e}')

        return dfs