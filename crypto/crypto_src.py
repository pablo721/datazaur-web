import requests
import os
from django.conf import settings
import ccxt
from pycoingecko import CoinGeckoAPI
from sqlalchemy import create_engine
from forex_python.converter import CurrencyRates
from markets.models import Ticker
from markets.utils import convert_rate
from .models import *
from src.utils.decorators import load_or_save
from src.utils.formatting import *

from config import constants

CURRENCY = constants.DEFAULT_CURRENCY
API_KEY = os.environ.get("CRYPTOCOMPARE_API_KEY")


def gecko_quote(base, quote):
    gecko = CoinGeckoAPI()
    coin = Cryptocurrency.objects.get(symbol=base).coin_id
    data = gecko.get_coin_by_id(coin)['market_data']
    price = data['current_price'][quote]
    mcap = data['market_cap']
    daily_chg = data['price_change_percentage_24h']
    weekly_chg = data['price_change_percentage_7d']
    monthly_chg = data['price_change_percentage_30d']
    yearly_chg = data['price_change_percentage_1y']
    return coin, price, mcap, daily_chg, weekly_chg, monthly_chg, yearly_chg


def find_quotes(base, quote, exchanges):
    quotes = {}
    ticker = base.upper() + '/' + quote.upper()
    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
        markets = pd.DataFrame(exchange.load_markets()).transpose()
        if ticker in markets.index:
            quotes[exchange_id] = exchange.fetch_ticker(ticker)['last']
    return quotes


def get_coins_info():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={API_KEY}'
    data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
                                                                       'FullName', 'Description', 'Algorithm',
                                                                       'ProofType', 'TotalCoinsMined',
                                                                       'CirculatingSupply', 'MaxSupply',
                                                                       'BlockReward', 'AssetWebsiteUrl',
                                                                       'IsUsedInDefi', 'IsUsedInNft']]
    return data


def get_coin_price(symbol, quote):
    if quote != 'USD':
        rate = convert_rate('USD', quote)
    else:
        rate = 1
    if Ticker.objects.filter(base=symbol).filter(quote=quote).exists():
        bid_price = Ticker.objects.get(base=symbol, quote=quote).bid
        ask_price = Ticker.objects.get(base=symbol, quote=quote).ask
        if bid_price:
            return [bid_price * rate, ask_price * rate if ask_price else 0]
    else:
        pass


def update_coin_prices(currency='USD'):
    n_new = 0
    n_upd = 0
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={API_KEY}'
    cols = ['CoinInfo.Name', f'RAW.{currency}.PRICE', f'RAW.{currency}.TOTALVOLUME24H',
            f'RAW.{currency}.HIGH24HOUR', f'RAW.{currency}.LOW24HOUR',
            f'RAW.{currency}.CHANGE24HOUR']

    df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
    df.columns = ['base', 'bid', 'daily_vol', 'daily_high', 'daily_low', 'daily_delta']
    df['quote'] = currency
    df['ask'] = 0
    for i, r in df.iterrows():
        if not Ticker.objects.filter(base=r['base'].upper()).filter(quote=currency).exists():
            Ticker.objects.create(**r)
            n_new += 1
        else:
            ticker = Ticker.objects.filter(base=r['base']).filter(quote=currency)[0]
            ticker.__dict__.update(**r)
            ticker.save()
            n_upd += 1
        print(str({**r}))
    print(f'Created {n_new} tickers \n ' f'Updated prices of {n_upd} tickers')


# @load_or_save('crypto.files', 1200)


def top_coins_by_mcap(currency='USD'):
    db_url = os.environ.get('LOCAL_DB_URL')
    engine = create_engine(url)
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={API_KEY}'
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
    df.to_sql('top_coins', engine, 'crypto', if_exists='replace')


@load_or_save('exchanges.files', 86400)
def exchanges_by_vol():
    url = f'https://min-api.cryptocompare.com/data/exchanges/general?api_key={API_KEY}&tsym={CURRENCY}'
    df = pd.DataFrame(requests.get(url).json()['Data']).transpose()[
        ['Name', 'Country', 'Grade', 'TOTALVOLUME24H', 'AffiliateURL']]
    df['Name'] = df.apply(lambda x: f"""<a href={x['AffiliateURL']}>{x['Name']}</a>""", axis=1)
    df['24h vol (BTC)'] = df['TOTALVOLUME24H'].apply(lambda x: x['BTC'], True).round(3)
    df[f'24h vol ({CURRENCY})'] = df['TOTALVOLUME24H'].apply(lambda x: '%.3f' % x[CURRENCY], True)
    df = df.drop(['TOTALVOLUME24H', 'AffiliateURL'], axis=1).sort_values(by='24h vol (BTC)',
                                                                         ascending=False).reset_index(drop=True)
    vol_col = f'Volume ({CURRENCY})'
    df.columns = ['Name', 'Country', 'Grade', vol_col, 'Url']
    df.drop('Url', axis=1, inplace=True)
    df[vol_col] = list(map(lambda x: format(x, ','), df[vol_col]))
    return df







def market_dominance(top_n_coins):
    filename = '~/PycharmProjects/datazaur_web/crypto.files'
    coins = pd.read_csv(filename, index_col=0).loc[:top_n_coins, f'Market cap ({CURRENCY})']
