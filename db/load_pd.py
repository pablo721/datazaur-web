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



def crypto_global_metrics():
    url = 'https://api.coingecko.com/api/v3/global'
    df = json.loads(requests.get(url).text)['data']
    df2 = pd.DataFrame(data={'total_market_cap': df.pop('total_market_cap'),
                             'market_cap_percentage': df.pop('market_cap_percentage'),
                             'total_volume': df.pop('total_volume')
                             })








def load_indices():
    countries = investpy.get_index_countries()

    for country in countries:
        df = investpy.indices.get_indices(country)
        df.to_sql('indices', engine, 'markets', if_exists='replace', index=False)


def load_indices_values():
    engine.execute('truncate table markets_indices2;')
    for country in investpy.get_index_countries():
        try:
            df = investpy.get_indices_overview(country)
            df.to_sql('indices_values', engine, 'markets', if_exists='append', index=False)

        except Exception as e:
            print(f'Error {e} while loading indices for country {country}.')
        finally:
            time.sleep(1)




def wb_regions():
    regions = pd.DataFrame(json.loads(requests.get('http://api.worldbank.org/v2/region?format=json').text)[1]).iloc[:, 1:]
    regions.to_sql('region', engine, 'macro', if_exists='replace', index=False)


def wb_topics():
    topics = pd.DataFrame(json.loads(requests.get('http://api.worldbank.org/v2/topic?format=json').text)[1])
    topics.to_sql('topic', engine, 'macro', if_exists='replace', index=False)


def wb_incomelevels():
    levels = pd.DataFrame(json.loads(requests.get('http://api.worldbank.org/v2/incomelevel?format=json').text)[1])
    levels.to_sql('incomelevel', engine, 'macro', if_exists='replace', index=False)


def wb_lendingtypes():
    types = pd.DataFrame(json.loads(requests.get('http://api.worldbank.org/v2/lendingtypes?format=json').text)[1])
    types.to_sql('lendingtype', engine, 'macro', if_exists='replace', index=False)


def wb_countries():
    n = Country.objects.all().count()
    countries = wb.get_countries()
    countries.columns = ['iso3c', 'id', 'name', 'region', 'adminregion', 'incomeLevel', 'lendingType',
                         'capitalCity', 'longitude', 'latitude']
    countries['currency_code'] = ""
    countries.to_sql('country', engine, 'macro', if_exists='replace', index=False)



def wb_sources():
    page1 = json.loads(requests.get('http://api.worldbank.org/v2/source?format=json&page=1').text)[1]
    page2 = json.loads(requests.get('http://api.worldbank.org/v2/source?format=json&page=2').text)[1]
    sources = page1 + page2
    df = pd.DataFrame(sources)
    df.to_sql('source', engine, 'macro', if_exists='replace', index=False)


def wb_indicators():
    indicators = wb.get_indicators()
    indicators.drop(labels=['sourceOrganization', 'unit'], axis=1, inplace=True)
    indicators.to_sql('indicator', engine, 'macro', if_exists='replace', index=False)





def load_finnhub_countries():
    url = f"https://finnhub.io/api/v1/country?token=cbcepm2ad3ib4g5ukl2g"
    df = pd.DataFrame(json.loads(requests.get(url).text))
    df.to_sql('macro_finnhub_countries', engine, if_exists='replace', index=False)



def load_bonds():
    with engine.connect() as conn:
        conn.execute('truncate table markets_bonds;')
        for country in investpy.get_bond_countries():
            try:
                bonds = investpy.get_bonds_overview(country)
                bonds.to_sql('markets_bonds', conn, if_exists='append', index=False)
                print(f'Saved bonds: {bonds}')
            except Exception as e:
                print(f'Error: {e}')
            time.sleep(1)







def corporate_bitcoin_holdings():
    url = 'https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin'
    holdings = pd.DataFrame(json.loads(requests.get(url).text))
    holdings2 = pd.DataFrame(list(holdings['companies']))
    holdings2.to_sql('crypto_corporate_btc_holdings', engine, if_exists='replace', index=False)


def corporate_eth_holdings():
    url = 'https://api.coingecko.com/api/v3/companies/public_treasury/ethereum'
    holdings = pd.DataFrame(json.loads(requests.get(url).text))
    holdings2 = pd.DataFrame(list(holdings['companies']))
    holdings2.to_sql('crypto_corporate_eth_holdings', engine, if_exists='replace', index=False)



def stock_gainers():
    url = f'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={finmodel_key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    df.to_sql('markets_stocks_gainers', engine, if_exists='replace', index=False)


def stock_losers():
    url = f'https://financialmodelingprep.com/api/v3/stock_market/losers?apikey={finmodel_key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    df.to_sql('markets_stocks_losers', engine, if_exists='replace', index=False)



def trending_crypto():
    url = 'https://api.coingecko.com/api/v3/search/trending'
    data = json.loads(requests.get(url).text)['coins']
    df = []
    for item in data:
        df.append(item['item'])
    df = pd.DataFrame(df)
    df.to_sql('markets_trending_crypto', engine, if_exists='replace', index=False)


