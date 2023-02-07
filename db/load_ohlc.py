import pandas as pd
import requests
import json


# yfinance
# investpy
# financialmodeling
#


# interval - e.g. 1hour
def ohlc_finmodeling(symbol, interval):
    key = 'fe6b9480f1fe2fa7d2b589cf7cd6f297'
    url = f'https://financialmodelingprep.com/api/v3/historical-chart/{interval}/{symbol}?apikey={key}'





def yahoo_stock(ticker, start, end):
    return web.DataReader(ticker, 'yahoo', start, end)

