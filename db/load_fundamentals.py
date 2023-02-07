import requests
import json
import pandas as pd
import yfinance

symbol = 'IBM'
alpha_key = '1WEDCC91HCX5F7U4'
finmodel_key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'


def profile_finmodeling(symbol):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)
    print(df.columns)
    df.to_csv('prof_finmodel.csv')


def profile_yahoo(symbol):
    return yfinance.Ticker(symbol)


def profile_alpha(symbol):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_key}'
    r = requests.get(url)
    data = r.json()
    print(data)



def company_full_info(symbol, since):
    today = datetime.date.today()
    if not since:
        since = today - datetime.timedelta(days=365)
    results = {}
    token = 'cbcepm2ad3ib4g5ukl2g'

    results['company_profile'] = profile_finmodeling(symbol)
    results['insider_transactions'] = load_insider_trades(symbol)
    results['insider_sentiment'] = load_insider_sentiment(symbol, str(since), str(today))
    results['financials'] = load_financials(symbol)
    results['social_sentiment'] = load_social_sentiment(symbol)
    results['senate_lobbying'] = load_senate_lobbying(symbol, str(since), str(today))
    results['us_spending'] = load_us_spending(symbol, str(since), str(today))
    results['company_news'] = load_company_news(symbol, str(since), str(today))



def load_insider_trades(symbol):
    token = 'cbcepm2ad3ib4g5ukl2g'
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={token}"
    df = pd.DataFrame(json.loads(requests.get(url).text)['data'])
    return df



def load_insider_sentiment(symbol, start_date='2015-01-01', end_date='2022-03-01'):
    token = 'cbcepm2ad3ib4g5ukl2g'
    url = f"https://finnhub.io/api/v1/stock/insider-sentiment?symbol={symbol}&from={start_date}&to={end_date}&token={token}"
    df = pd.DataFrame(json.loads(requests.get(url).text)['data'])
    return df


def yahoo_options(symbol):
    return Options(symbol).get_all_data()



def quote_finmodeling(symbol):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)
    print(df.columns)



def load_fin_statements_list():
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)




def load_finratios_finmodeling(symbol):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)



def load_key_metrics_finmodeling(symbol):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=40&apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)


def company_income_statement(symbol):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=120&apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)


def load_finnhub_earnings(symbol):
    url = f"https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token=cbcepm2ad3ib4g5ukl2g"
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)



def load_enterprise_value(symbol):
    url = f'https://financialmodelingprep.com/api/v3/enterprise-values/{symbol}?limit=40&apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)



def load_finnhub_recommendations(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token=cbcepm2ad3ib4g5ukl2g"
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)



def load_institutional_holders(symbol):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v4/institutional-ownership/institutional-holders/symbol-ownership-percent?date=2021-09-30&symbol={symbol}&page=0&apikey={key}'
    df = pd.DataFrame(json.loads(requests.get(url).text))
    print(df)



def sentiment_news(symbol):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&topics=technology&apikey={alpha_key}'
    r = requests.get(url)
    data = pd.DataFrame(r.json())
    feed_data = pd.DataFrame(data=pd.DataFrame(list(data['feed'])), columns=data.loc[0, 'feed'].keys())
    feed_data['authors'] = feed_data['authors'].apply(lambda x: str(x))
    feed_data['ticker_sentiment'] = [pd.DataFrame(x) for x in feed_data['ticker_sentiment'].values]
    feed_data['topics'] = [pd.DataFrame(x, columns=['topic', 'relevance_score']) for x in feed_data['topics']]
    return feed_data
