import ccxt
from crypto.models import CryptoExchange, Cryptocurrency
from pycoingecko import CoinGeckoAPI
import pandas as pd
import json
import requests
from config import constants
from monitor.models import Ticker
import datetime

def get_coins_info():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={API_KEY}'
    data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
                                                                       'FullName', 'Description', 'Algorithm',
                                                                       'ProofType', 'TotalCoinsMined',
                                                                       'CirculatingSupply', 'MaxSupply',
                                                                       'BlockReward', 'AssetWebsiteUrl',
                                                                       'IsUsedInDefi', 'IsUsedInNft']]
    return data


def load_cryptocomp_coins():
    n = Cryptocurrency.objects.all().count()
    coins = get_coins_info().loc[:, ['Symbol', 'CoinName', 'Description', 'Algorithm', 'ProofType', 'AssetWebsiteUrl']]
    coins.columns = ['symbol', 'name', 'description', 'hash_algorithm', 'proof_type', 'url']
    coins[['description', 'url']] = coins[['description', 'url']].apply(lambda x: x[:254])
    for i, row in coins.iterrows():
        if not Cryptocurrency.objects.filter(symbol__iexact=row['symbol']).exists():
            Cryptocurrency.objects.create(name=row['name'], symbol=row['symbol'],
                                          url=str(row['url'])[:254] if row['url'] else '',
                                          description=str(row['description'])[:254] if row['description'] else '',
                                          hash_algorithm=row['hash_algorithm'], proof_type=row['proof_type'])

    print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptocurrencies from Cryptocompare.')


def load_gecko_coins():
    n = Cryptocurrency.objects.all().count()
    gecko = CoinGeckoAPI()
    coins_list = gecko.get_coins_list()
    for coin in coins_list:
        if not Cryptocurrency.objects.filter(symbol=coin['symbol']).exists():
            Cryptocurrency.objects.create(symbol=coin['symbol'], name=coin['name'].lower())
    print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptos from CoinGecko.')



def load_crypto_exchanges():
    n = 0
    for exchange_id in ccxt.exchanges:
        exchange_obj = getattr(ccxt, exchange_id)()
        if CryptoExchange.objects.filter(name=exchange_id).exists():
            CryptoExchange.objects.filter(name=exchange_id).update(url=exchange_obj.urls['www'])
        else:
            CryptoExchange.objects.create(name=exchange_id, url=exchange_obj.urls['www'])
            n += 1
    print(f'Loaded {n} exchanges to database.')



def load_crypto_tickers():
    count = 0
    exchanges = constants.DEFAULT_CRYPTO_EXCHANGES
    for exchange in exchanges:
        exchange_obj = getattr(ccxt, exchange)({'enableRateLimit': True})
        tickers = pd.DataFrame(exchange_obj.load_markets()).transpose()
        for i, row in tickers.iterrows():
            base = row['base']
            quote = row['quote']
            if not Ticker.objects.filter(base_symbol=base, quote_symbol=quote, source=exchange_obj.id).exists():
                Ticker.objects.create(base_symbol=base, quote_symbol=quote, source=exchange_obj.id, source_type='crypto_exchange')
                count += 1
                print(f'Created ticker: {base}/{quote}. Source: {exchange_obj.id}')
    print(f'Added {count} tickers from exchanges: {exchanges}')


def update_crypto_prices():
    count = 0
    upd_count = 0
    exchanges = constants.DEFAULT_CRYPTO_EXCHANGES
    for exchange in exchanges:
        try:
            exchange_obj = getattr(ccxt, exchange)({'enableRateLimit': True})
            tickers = pd.DataFrame(exchange_obj.fetch_tickers()).transpose()
            source = exchange_obj.id
            now = datetime.datetime.now()
            print(f'{source}: {len(tickers)} tickers.')
            for i, row in tickers.iterrows():
                if '/' not in i:
                    continue
                base = i.split('/')[0]
                quote = i.split('/')[1]
                bid = row['bid']
                ask = row['ask']
                last = row['last']
                if not Ticker.objects.filter(base_symbol=base, quote_symbol=quote, source=source).exists():
                    Ticker.objects.create(base_symbol=base, quote_symbol=quote, source=source, price=last, bid=bid, ask=ask, timestamp=now)
                    count += 1
                    print(f'Created ticker: {base}/{quote}. \nPrice: {bid} \n Source: {source}')
                else:
                    Ticker.objects.filter(base_symbol=base, quote_symbol=quote, source=source).update(price=last, bid=bid, ask=ask, timestamp=now)
                    upd_count += 1
        except Exception as e:
            print(f'Error: {e}')

    print(f'Added {count} and updated {upd_count} tickers from exchanges: {exchanges}')

#
#
# finmodel_crypto = f'https://financialmodelingprep.com/api/v3/symbol/available-cryptocurrencies?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'
#
# #np binance
# finhub_coins = f"https://finnhub.io/api/v1/crypto/symbol?exchange={exchange}&token=cbcepm2ad3ib4g5ukl2g"