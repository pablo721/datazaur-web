import ccxt
import pandas as pd
import re

from markets.models import Ticker


def connect_exchange(exchange_id):
	return getattr(ccxt, exchange_id)({'enableRateLimit': True})



def coin_prices_from_exchanges(coins, quote, exchange_ids):
	tickers = [coin + '/' + quote for coin in coins]
	result = pd.DataFrame(index=tickers, columns=['bid', 'ask', 'daily_delta', 'daily_pct_delta',
								'daily_vol', 'daily_low', 'daily_high', 'source', 'timestamp'])

	for exchange_id in exchange_ids:
		exchange = connect_exchange(exchange_id)
		markets = pd.DataFrame(exchange.load_markets()).transpose()
		print(f'markets: {markets.index}')
		found_tickers = [ticker for ticker in tickers if ticker in markets.index]
		print(f'tickers: {found_tickers}')
		prices = exchange.fetch_tickers(tickers)
		print(f'prices: {prices}')

		for ticker, data in prices.items():
			try:
				result.loc[ticker] = {'bid': data['bid'], 'ask': data['ask'], 'daily_delta': data['change'],
									  'daily_pct_delta': data['percentage'], 'daily_vol': data['quoteVolume'],
									  'daily_low': data['lowPrice'], 'daily_high': data['highPrice'], 'source': exchange_id,
									  'timestamp': data['datetime']}
				tickers.remove(ticker)

			except:
				pass
	print(result)
	return result


def load_coin_prices_to_db(coins, quote, exchange_ids):
	prices = coin_prices_from_exchanges(coins, quote, exchange_ids)
	for i, row in prices.iterrows():
		base = i.split('/')[0]
		quote = i.split('/')[1]
		if Ticker.objects.filter(base=base).filter(quote=quote).exists():
			ticker = Ticker.objects.get(base=base, quote=quote).__dict__
		else:
			ticker = Ticker.objects.create(base=base, quote=quote, base_asset_class='crypto')

		ticker.update(**row)
		ticker.save()
		print(ticker.__dict__)



def load_coin_price_history(ticker, start_date, end_date, exchange_id):
	pass







def update_fx_rates(base='USD'):
	rates = investpy.get_currency_crosses_overview(base, False, 1000)
	for i, row in rates.iterrows():
		print(row)
		if '/' not in row['symbol']:
			continue
		base = row['symbol'].split('/')[0]
		quote = row['symbol'].split('/')[1]
		if Ticker.objects.filter(base=base).filter(quote=quote).exists():
			ticker = Ticker.objects.get(base=base, quote=quote)
		else:
			ticker = Ticker.objects.create(base=base, quote=quote)

		ticker.bid = row['bid']
		ticker.ask = row['ask']
		ticker.mid = (row['bid'] + row['ask']) / 2
		ticker.daily_delta = row['change']
		ticker.daily_delta_pct = row['change_percentage']
		ticker.daily_low = row['low']
		ticker.daily_high = row['high']

		ticker.save()




