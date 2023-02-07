import pandas as pd
import random


def get_random_color():
	rgb_color = []
	for i in range(3):
		rgb_color.append(hex(random.randint(0, 155))[2:])
	return '#' + ''.join(rgb_color)


def round_number(x, n):
	x2 = float(x.replace('%', '').replace('+', '')) if type(x) == str else x
	return x2.__round__(n)


def add_hyperlinks(df):
	url = 'https://cryptocompare.com'
	for col in ['Symbol', 'Name']:
		df[col] = df.apply(lambda x: f"""<a href={url + x['Url']}>{x[col]}</a>""", axis=1)
	return df


def add_yields_hyperlinks(x):
	return f"""<a href='/yield_curves?country={x}'> {x.title()} </a>"""


def string_to_float(x):
	if type(x) == str:
		return float(x.replace('%', '').replace('+', ''))



def color_cell2(x):
	if x > 0:
		prefix, color = ('+', 'green')
	elif x < 0:
		prefix, color = ('', 'red')
	else:
		prefix, color = ('', 'white')
	return f"""<p class={color}>{prefix}{str(x.__round__(2))}%</p>"""


def color_cell(x):
	sign = str(x)[0]
	prefix, color = ('', 'red') if sign == '-' else ('+', 'green')
	return f"""<p class={color}>{prefix}{x}</p>"""


def prepare_df_display(df, n_decimals=2):
	for col in df.columns:
		if 'Price' in col or 'Δ' in col or 'vol' in col or 'cap' in col or 'Supply' in col:
			df[col] = df[col].apply(
				lambda x: format(float(x.replace(',', '')).__round__(n_decimals), ',') if type(x) == str else
				format(float(x).__round__(n_decimals), ','))
			if 'Δ' in col:
				df[col] = df[col].apply(lambda x: f'{x}%')
				df[col] = df[col].apply(color_cell)

	if 'Url' in df.columns:
		df = add_hyperlinks(df)
		df.drop('Url', inplace=True, axis=1)

	if 'Updated' in df.columns:
		df['Updated'] = df['Updated'].apply(lambda x: pd.to_datetime(x * 10 ** 9))
	return df



def prepare_df_save(df, currency):
	df.columns = ['Symbol', 'Name', 'Url', 'Price', '24h Δ', '1h %Δ', '24h %Δ', '24h vol', f'Market cap ({currency})',
				  'Supply', 'Updated']
	df.dropna(inplace=True)
	df.iloc[:, 7:9] = df.iloc[:, 7:9].astype('int64')
	return df


def prep_market_df(df, n_decimals=3):
	df.columns = ['Symbol', 'Price', '24h Δ'] if len(df.columns) == 3 else ['Symbol', 'Price', '24h Δ', '24h %Δ']
	df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: float(str(x).replace('%', '').replace('+', ''))).round(
		n_decimals).applymap(lambda x: format(x, ','))
	if '24h %Δ' in df.columns:
		df['24h %Δ'] = df['24h %Δ'].apply(lambda x: f'{x}%')
	df.iloc[:, 2:] = df.iloc[:, 2:].applymap(color_cell)

	return df
