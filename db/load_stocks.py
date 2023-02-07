import pandas as pd
import json
import requests
import time
from markets.models import Exchange, Stock, Currency


def load_exchanges():
    n = 0
    file = './config/exchanges.csv'
    df = pd.read_csv(file)
    print(f'Exhanges: {df}')
    for i, row in df.iterrows():
        if not Exchange.objects.filter(code=row['code']).exists():
            Exchange.objects.create(name=row['name'], code=row['code'], mic=row['mic'], timezone=row['timezone'],
                                    hours=row['hour'], country_code=row['country'], source=row['source'])
            print(f'Exchange added: {row}')
            n += 1
    print(f'Loaded {n} exchanges.')


def load_stocks_finnhub():
    n = 0
    for exchange in Exchange.objects.all():

        token = 'cbcepm2ad3ib4g5ukl2g'
        url = f"https://finnhub.io/api/v1/stock/symbol?exchange={exchange.code}&token={token}"
        df = pd.DataFrame(json.loads(requests.get(url).text))
        print(f'Loaded stocks: {df}')
        for i, row in df.iterrows():
            try:
                stock = Stock.objects.create(exchange=exchange)
                stock.currency_id = row['currency']
                for k, v in row.items():
                    try:
                        stock.__dict__[k] = v
                    except Exception as e:
                        print(f'Error: {e}')
                if stock.symbol:
                    stock.displaySymbol = stock.symbol.split('.')[0]
                elif stock.displaySymbol:
                    stock.displaySymbol = stock.displaySymbol.split('.')[0]

                n += 1
                stock.save()
            except Exception as e:
                print(f'Error {e} when loading stock {row.description}')


        print(f'Loaded {len(df)} symbols from {exchange.name}.')
        time.sleep(1)
    print(f'Loaded {n} stock symbols from {Exchange.objects.all().count()} exchanges.')






def load_tsx_stocks():
    url = f'https://financialmodelingprep.com/api/v3/symbol/available-tsx?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'


def load_nasdaq_symbols():
    return get_nasdaq_symbols()



def load_etfs_finmodeling():
    url = f'https://financialmodelingprep.com/api/v3/etf/list?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)




def load_all_fin_statements():
    url = f'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'



def tradeable_stocks_finmodeling():
    url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)
    df.to_csv('stonks.csv', index=False)


def load_stocks_finmodeling():
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'
    df = pd.DataFrame(json.loads(requests.get(url).text))

    print(df)
    df.to_csv('stonks6.csv', index=False)



def load_funds_list():
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v4/institutional-ownership/list?apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)






url = f'https://financialmodelingprep.com/api/v3/fx?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'