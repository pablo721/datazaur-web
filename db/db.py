import investpy
import pandas as pd
import pycountry
import country_currencies
import requests
import ccxt
import time
from pycoingecko import CoinGeckoAPI
import yaml
import json
import re
from macro.models import Country
from markets.models import Ticker, Commodity, Currency, Index, Exchange, Stock
from news.models import Website, Article
from website.models import Account
from datawarehouse.models import Log, Config, UpdateTime
from crypto.models import CryptoExchange, Cryptocurrency
from calendar_.models import MacroCalendar, CryptoCalendar

from config import constants
from crypto.crypto_src import get_coins_info
import datetime

token = 'cbcepm2ad3ib4g5ukl2g'



def setup_stonks():
	load_exchanges()
	load_stock_symbols()


def setup_news():
	load_crypto_articles()
	finnhub_news()
	load_econ_calendar()


def setup_all():
	funcs = [load_config, load_countries, load_currencies, map_currencies, load_fx_tickers, update_fx_prices,      #load_crypto_tickers,
			 load_crypto_exchanges, load_cryptocomp_coins, update_crypto_prices, load_indices, load_econ_calendar,
			 load_crypto_articles, load_exchanges, finnhub_news,
			 ]
	tables = ['website_log', 'markets_country', 'markets_currency', 'markets_currency', 'markets_ticker', 'markets_ticker',   # 'markets_ticker',
			  'crypto_cryptoexchange', 'crypto_cryptocurrency', 'markets_ticker', 'markets_index', 'calendar_econevent',
			  'news_article', 'markets_exchange', 'news_article']
	timestamp = datetime.datetime.now()
	for func, table in zip(funcs, tables):
		try:
			print(f'setting: {table}')
			func()
			if not Update.objects.filter(table=table).exists():
				Update.objects.create(table=table, timestamp=timestamp)
			update = Update.objects.get(table=table)
			update.timestamp = timestamp
			update.save()
			Log.objects.create(source=table, timestamp=timestamp, status=0)

		except Exception as e:
			print(f'Error: {e}')
			Log.objects.create(source=table, timestamp=timestamp, status=1, message=f'Error: {e}')

	print(f'Finito setup.')


def load_websites(filepath='config/websites.yaml'):
	with open(filepath, 'r') as file:
		websites = yaml.safe_load(file)
		for k, v in websites.items():
			print(f'Site {k}')
			print(f'Selectors {v}')
			if not Website.objects.filter(url=k).exists():
				Website.objects.create(url=k)
			site = Website.objects.get(url=k)
			for selector in v:
				if not Selector.objects.filter(text=selector).exists():
					Selector.objects.create(text=selector)
				s = Selector.objects.get(text=selector)
				site.selectors.add(s)
				site.save()
				print(f'Loaded {len(v)} selectors for {k}')


def load_config(filepath='config/config.yaml'):
	ext = filepath.split('.')[-1].lower()
	with open(filepath, 'r') as cfg:
		if ext == 'json':
			cfg_data = json.load(cfg.read())
		elif ext in ['yaml', 'yml']:
			cfg_data = yaml.safe_load(cfg)
		else:
			return 'Wrong file type. \n ' \
				   'Need a json/yaml/yml config file.'

	n_upd = 0
	n = Config.objects.all().count()
	for k, v in cfg_data.items():
		if Config.objects.filter(key=k).exists():
			cfg = Config.objects.get(key=k)
			cfg.value = v
			cfg.save()
			n_upd += 1
		else:
			Config.objects.create(key=k, value=v)
	print(f'Added {Config.objects.all().count() - n} parameters to database. \n'
		  f'Updated {n_upd} parameters.')





def connect_exchange(exchange_id, quote='USDT'):
	exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
	return pd.DataFrame(exchange.fetch_tickers()).transpose()


def filter_by_quote(ticker, quote='USDT'):
	return ticker.split('/')[1].__eq__(quote)



def load_fx_tickers():
	source = 'investing.com'
	crosses = investpy.get_currency_crosses()
	for i, row in crosses.iterrows():
		if not Ticker.objects.filter(base=row['base'], quote=row['second'], source=source).exists():
			Ticker.objects.create(base=row['base'], quote=row['second'], source=source)




def update_fx_prices():
	quote_curr = constants.DEFAULT_CURRENCY
	n_created = 0
	n_updated = 0
	source = 'investing.com'
	now = datetime.datetime.now()
	df = investpy.get_currency_crosses_overview(quote_curr, n_results=300)
	for i, row in df.iterrows():
		if '/' not in row['symbol']:
			continue
		base = row['symbol'].split('/')[0]
		quote = row['symbol'].split('/')[1]
		if Ticker.objects.filter(base=base, quote=quote, source=source).exists():
			Ticker.objects.filter(base=base, quote=quote, source=source).update(bid=row['bid'], ask=row['ask'],
										   timestamp=now)
			n_updated += 1
		else:
			Ticker.objects.create(base=base, quote=quote, bid=row['bid'], ask=row['ask'], source=source,
										   timestamp=now)
			n_created += 1


	print(f'Created {n_created} new FX quotes. \nUpdated {n_updated} FX quotes.')


















