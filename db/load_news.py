import investpy
import sqlalchemy
from pandas_datareader import wb
import pandas_datareader.data as web
import time
import pandas as pd
import json
import requests
import csv
from .alchemy_utils import get_connection_string
from macro.models import Country




alpha_key = '1WEDCC91HCX5F7U4'
finmodel_key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
username = 'zaur'
password = 'wsad1221'
conn_string = get_connection_string('postgresql', 'psycopg2', username, password, 'localhost', '5432', 'zaurdb2')
engine = sqlalchemy.create_engine(conn_string)


def load_finnhub_news():
    token = 'cbcepm2ad3ib4g5ukl2g'
    url = f"https://finnhub.io/api/v1/news?category=general&token={token}"
    news = pd.DataFrame(json.loads(requests.get(url).text))
    news.to_sql('news_finnhub_news', engine, if_exists='replace', index=False)


def load_crypto_news():
    api_key = '70d54fd6e56db84eba0a9d9166b4d5da087c79d3d6cc0511e69144270f90c09b'
    url = f'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={api_key}'
    news = pd.DataFrame(json.loads(requests.get(url).text)['Data'])
    news = news.iloc[:, :10]
    news.to_sql('news_crypto_news', engine, if_exists='replace', index=False)



def crypto_news_feed():
    api_key = '70d54fd6e56db84eba0a9d9166b4d5da087c79d3d6cc0511e69144270f90c09b'
    url = f'https://min-api.cryptocompare.com/data/news/feeds?lang=EN&api_key={api_key}'
    feed = pd.DataFrame(json.loads(requests.get(url).text))
    feed.to_sql('news_crypto_feed', engine, if_exists='replace', index=False)
