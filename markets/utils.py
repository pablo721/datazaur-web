from markets.models import Currency, Ticker
from forex_python.converter import CurrencyRates
from config import constants
from datawarehouse.models import Config

default = constants.DEFAULT_CURRENCY




def convert_rate(src_curr, dst_curr):
	if Ticker.objects.filter(base=src_curr).filter(quote=dst_curr).exists():
		ticker = Ticker.objects.get(base=src_curr, quote=dst_curr)
		rate = ticker.bid
		print(1)
	else:
		rates = CurrencyRates()
		rate = rates.get_rate(src_curr, dst_curr)
		print(2)
	return rate


def ordered_currencies(code=default):
	first = code.upper()
	if not Currency.objects.filter(alpha_3=first).exists():
		return f'No currency matches {first}'
	first_curr = Currency.objects.filter(alpha_3=first)
	all_currs = Currency.objects.all().exclude(alpha_3=first)
	return first_curr.union(all_currs, all=True)



def convert_fx(df, price_cols, src_curr, dst_curr):
	print(price_cols)
	print(df.columns)
	rate = convert_rate(src_curr, dst_curr)
	print(f'fx rate {src_curr} to {dst_curr} is {rate}')
	if not rate:
		return f'cant find exchange rate: {src_curr}/{dst_curr}'

	print(df.dtypes)
	df.loc[:, price_cols] = df.loc[:, price_cols].applymap(lambda x: format((float(x.replace(',', '')) * rate).__round__(2), ','))

	df.currency = dst_curr

	print(f'Converted {src_curr} to {dst_curr} at rate {rate}')
	return df


def get_currency(request):
	code = 'USD'

	try:
		acc = request.user.user_account
		code = acc.currency_code
	except:
		acc = None

	if not acc:
		try:
			code = Config.objects.get(key='default_currency')
		except:
			pass

	currency = Currency.objects.get(symbol=code)
	return currency

