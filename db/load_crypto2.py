import ccxt
from pycoingecko import CoinGeckoAPI
import pandas as pd
import json
import requests
import datetime
from sqlalchemy import create_engine
import os

from config import constants
from crypto.models import CryptoExchange, Cryptocurrency, CryptoTicker





def load_all_crypto():
    for func in [bulk_load_gecko_coins, bulk_load_crypto_exchanges, bulk_load_crypto_tickers, bulk_update_crypto_prices,
                 load_top_coins]:
        try:
            print(f'Start {func.__name__}')
            func()
        except Exception as e:
            print(f'Error {e} at function {func.__name__}')






def load_top_coins(currency='USD'):
    db_url = os.environ.get('LOCAL_DB_URL')
    api_key = os.environ.get('CRYPTOCOMPARE_API_KEY')
    engine = create_engine(db_url)
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={api_key}'
    cols = f'CoinInfo.Name CoinInfo.FullName CoinInfo.Url RAW.{currency}.PRICE ' \
           f'RAW.{currency}.CHANGEPCTHOUR RAW.{currency}.CHANGEPCT24HOUR ' \
           f'RAW.{currency}.TOTALVOLUME24HTO ' \
           f'RAW.{currency}.MKTCAP RAW.{currency}.SUPPLY RAW.{currency}.LASTUPDATE'.split()
    df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
    df.columns = ['Symbol', 'Name', 'Url', 'Price', '1h Δ', '24h Δ', '24h vol', f'Market cap ({currency})',
                  'Supply', 'Updated']
    df.dropna(inplace=True)
    df.iloc[:, 3:6] = df.iloc[:, 3:6].astype('float64').round(3)
    df.iloc[:, 6:9] = df.iloc[:, 6:9].astype('int64')
    df.currency = currency
    df.to_sql('top_coins', engine, 'public', if_exists='replace')


def load_gecko_coins(truncate=True):
    #engine = create_engine(db_url)
    if truncate:
        try:
            Cryptocurrency.objects.all().delete()
        except Exception as e:
            print(f'Exception: {e}')
    gecko = CoinGeckoAPI()
    return pd.DataFrame(gecko.get_coins_list()).drop_duplicates('symbol')



def bulk_load_gecko_coins(truncate=True):
    if truncate:
        Cryptocurrency.objects.all().delete()
    n = Cryptocurrency.objects.all().count()
    gecko = CoinGeckoAPI()
    coins_df = pd.DataFrame(gecko.get_coins_list()).drop_duplicates('symbol')
    coins_bulk = []
    for i, row in coins_df.iterrows():
        coin = Cryptocurrency(symbol=row['symbol'], name=row['name'].lower())
        coins_bulk.append(coin)
    Cryptocurrency.objects.bulk_create(coins_bulk)
    print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptos from CoinGecko.')



def bulk_load_crypto_exchanges(truncate=True):
    if truncate:
        CryptoExchange.objects.all().delete()
    n = CryptoExchange.objects.all().count()
    bulk_exchanges = []
    for exchange_id in ccxt.exchanges:
        try:
            exchange_obj = getattr(ccxt, exchange_id)({'enableRateLimit': True})
            exchange = CryptoExchange(name=exchange_id, url=exchange_obj.urls['www'])
            bulk_exchanges.append(exchange)
        except Exception as e:
            print(f'Error {e} while loading crypto exchanges')
    CryptoExchange.objects.bulk_create(bulk_exchanges)
    print(f'Loaded {CryptoExchange.objects.all().count() - n} exchanges to database.')



def bulk_load_crypto_tickers(truncate=True):
    exchanges = constants.DEFAULT_CRYPTO_EXCHANGES
    if truncate:
        CryptoTicker.objects.all().delete()

    count = CryptoTicker.objects.all().count()

    for exchange in exchanges:
        try:
            exchange_obj = getattr(ccxt, exchange)({'enableRateLimit': True})
            tickers = pd.DataFrame(exchange_obj.load_markets()).transpose()
            tickers1 = []
            for i, row in tickers.iterrows():
                base = row['base']
                quote = row['quote']
                source = exchange_obj.id
                ticker = CryptoTicker(base=base, quote=quote, source=source)
                tickers1.append(ticker)
            CryptoTicker.objects.bulk_create(tickers1)

        except Exception as e:
            print(f'Error: {e}')
    print(f'Added {CryptoTicker.objects.all().count() - count} tickers from exchanges: {exchanges}')


def bulk_update_crypto_prices():
    count = 0
    upd_count = 0
    exchanges = ['binance', 'kraken']
    for exchange in exchanges:
        try:
            exchange_obj = getattr(ccxt, exchange)({'enableRateLimit': True})
            print(1)
            tickers = pd.DataFrame(exchange_obj.fetch_tickers()).transpose()
            print(2)
            source = exchange_obj.id
            print(3)
            now = datetime.datetime.now()
            print(f'{source}: {len(tickers)} tickers.')
            tickers2 = []
            for i, row in tickers.iterrows():
                try:
                    if '/' not in i:
                        continue
                    base = i.split('/')[0]
                    quote = i.split('/')[1]
                    ticker = CryptoTicker.objects.filter(base=base, quote=quote, source=source).first()
                    ticker.price = row['last']
                    ticker.bid = row['bid']
                    ticker.ask = row['ask']
                    ticker.daily_delta = row['percentage']
                    ticker.timestamp = now
                    tickers2.append(ticker)
                    upd_count += 1
                except Exception as e:
                    print(f'Exception {e} when updating ticker {i} / {exchange}')

            CryptoTicker.objects.bulk_update(tickers2, fields=['price', 'bid', 'ask', 'daily_delta', 'timestamp'])

        except Exception as e:
            print(f'Error: {e}')

    print(f'Updated {upd_count} tickers from exchanges: {exchanges}')



def load_global_metrics():
    db_url = os.environ.get('LOCAL_DB_URL')
    engine = create_engine(db_url)
    gecko = CoinGeckoAPI()
    df = pd.DataFrame(gecko.get_global()).dropna(subset='market_cap_percentage')
    print(df)
    print(df.columns)
    df_dominance = df.loc[:, ['total_market_cap', 'total_volume', 'market_cap_percentage', 'updated_at']]
    df_metrics = pd.DataFrame(df.iloc[0, 1:5]).reset_index(drop=False)
    df_metrics.columns = ['metric', 'value']
    df_dominance.to_sql('crypto_dominance', engine, 'public', 'replace', index=True)
    df_metrics.to_sql('crypto_metrics', engine, 'public', 'replace', index=False)