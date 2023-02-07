import pandas as pd
import requests
import json




# daily
def sectors_performance2():
    finmodeling_sectors = f'https://financialmodelingprep.com/api/v3/sector-performance?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'
    df = pd.DataFrame(json.loads(requests.get(finmodeling_sectors).text))
    print(df)



finmodeling_url = f'https://financialmodelingprep.com/api/v4/insider/ownership/acquisition_of_beneficial_ownership?symbol=AAPL&apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'


finhub_crypto_excg = f"https://finnhub.io/api/v1/crypto/exchange?token=cbcepm2ad3ib4g5ukl2g"


url = f'https://financialmodelingprep.com/api/v3/fx?apikey=fe6b9480f1fe2fa7d2b589cf7cd6f297'

finhub_exchanges = f'https://finnhub.io/api/v1/forex/exchange?token=cbcepm2ad3ib4g5ukl2g'

# exchange np. oanda
finhub_fx = f"https://finnhub.io/api/v1/forex/symbol?exchange={exchange}&token=cbcepm2ad3ib4g5ukl2g"


def data_from_econdb(ticker):
    return web.DataReader(f'ticker={ticker}', 'econdb')


wb_population = 'http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2020?format=json'

wb_gdp = 'http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2020?format=json'
#from pandas_datareader.famafrench import get_available_datasets
#dat = wb.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
