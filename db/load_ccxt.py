import ccxt
import pandas as pd
import yaml
import json
from sqlalchemy import create_engine
import os


class CCXTLoader:
    INTERVALS = ['5m', '15m', '30m', '1h', '4h', '1d']

    def __init__(self):
        self.schedule = {}
        self.config = {}
        self.exchanges = {}
        self.engine = self.get_engine()

        self.load_config()

    def load_config(self):
        cfg_file = os.path.join(os.getcwd(), 'config', 'loader_config.yaml')
        with open(cfg_file) as f:
            cfg = yaml.safe_load(f)
            self.config.update(**cfg)

    def load_schedule(self):
        with open('schedule.yaml') as f:
            self.schedule = yaml.safe_load(f)

    def connect_exchange(self, exchange_id):
        if exchange_id not in self.exchanges.keys():
            exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
            self.exchanges[exchange_id] = exchange

        return self.exchanges[exchange_id]

    def get_engine(self):
        return create_engine(os.environ.get('LOCAL_DB_URL'), echo=True)

    @staticmethod
    def get_table_name(ticker, exchange_id, interval):
        return ticker + '_' + str(exchange_id) + '_' + interval

    def load_table(self, exchange_id, ticker, interval, limit=200):
        print(self.config)
        print(self.exchanges)
        exchange = self.connect_exchange(exchange_id)

        table_name = self.get_table_name(ticker, exchange_id, interval)
        df = pd.DataFrame(exchange.fetch_ohlcv(ticker, interval, limit=limit))
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df.set_index('timestamp').to_sql(table_name, self.engine, 'ohlc', if_exists='replace')

    def load_all_tables(self):
        for k, v in self.config.items():
            for ticker in v['tickers']:
                for interval in v['intervals']:
                    self.load_table(k, ticker, interval)

        print('Loaded all tables.')

    def load_crypto_exchanges(self):
        result = pd.DataFrame(columns=['name', 'url'])
        for exchange in ccxt.exchanges:
            exchange_obj = getattr(ccxt, exchange)()
            result[len(result)] = [exchange, exchange_obj.urls['www']]
        return result


    def load_crypto_tickers(self):
        result = pd.DataFrame(columns=['symbol', 'base', 'quote', 'source'])
        for exchange in ccxt.exchanges:
            try:
                exchange_obj = getattr(ccxt, exchange)({'enableRateLimit': True})
                tickers = pd.DataFrame(exchange_obj.load_markets()).transpose()[['symbol', 'base', 'quote']]
                tickers['source'] = exchange
                result = pd.concat([result, tickers])
            except Exception as e:
                print(f'Exception: {e}')
        return result

