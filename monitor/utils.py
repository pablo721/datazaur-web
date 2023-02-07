from .models import *
from crypto.models import *
from crypto.crypto_src import top_coins_by_mcap
from forex_python.converter import CurrencyRates
import pandas as pd


def generate_name(account):
	count = Watchlist.objects.filter(owner=account).count()
	return f'Watchlist {count + 1}'


def watchlist_prices(watchlist, quote):
	result = pd.DataFrame(index=[], data={'base': [], 'base_full_name': [], 'bid': [], 'ask': [], 'daily_delta': [], 'daily_pct_delta': [],
										  'daily_vol': [], 'daily_low': [], 'daily_high': []})
	result = []
	n = 0
	for ticker in watchlist.crypto_tickers.all():
		result.append(ticker.__dict__)
		n += 1
		print(ticker.__dict__)

	print(f'Found {n} out of {watchlist.crypto_tickers.all().count()} prices.')
	return result


def portfolio_prices(watchlist, quote):
	value = 0
	result = pd.DataFrame(index=[], data={'name': [], 'amount': [], 'bid': [], 'ask': [], 'daily_delta': [],
										  'daily_vol': [], 'daily_low': [], 'daily_high': []})
	n = 0
	for coin in portfolio.coins.all():
		if CryptoTicker.objects.filter(base=coin.symbol).filter(quote=quote).exists():
			n += 1
			result.loc[coin.symbol] = CryptoTicker.objects.get(base=coin.symbol, quote=quote).__dict__
			if Amounts.objects.filter(watchlist=watchlist).filter(coin=coin).exists():
				result.loc[coin.symbol, 'amount'] = Amounts.objects.get(watchlist=watchlist, coin=coin).amount
			print(result.loc[coin.symbol])
	print(f'Found {n} out of {watchlist.coins.all().count()} prices.')
	return result, value


def get_crypto_value(coin, quote, amount):
	coins = top_coins_by_mcap()

	if CURRENCY != quote:
		rates = CurrencyRates()
		exchange_rate = rates.get_rate(CURRENCY, quote)
	else:
		exchange_rate = 1

	price = coins[coins['Symbol'] == coin]['Price'].iloc[0]
	return amount * price * exchange_rate



def get_portfolio_value(portfolio, CURRENCY):
	value = 0
	currencies = settings.SORTED_CURRENCIES
	for k, v in portfolio.items():
		if k in currencies:
			value += get_crypto_value(k, CURRENCY, v)
		else:
			value += get_crypto_value(k, CURRENCY, v)

	return value