import investpy
import pandas as pd
import pycountry
import country_currencies
import requests
import ccxt
import time
import yaml
import json
import re
from macro.models import Country
from markets.models import Ticker, Asset, Commodity, Currency
from news.models import Website, Article
from website.models import Account
from datawarehouse.models import Log, Config, UpdateTime
from config import constants
from crypto.crypto_src import get_coins_info
import datetime



def load_countries():
    countries = pycountry.countries
    n = Country.objects.all().count()
    for obj in countries:
        if not Country.objects.filter(name=obj.name).exists():
            Country.objects.create(code=obj.alpha_2, name=obj.name)
    print(f'Loaded {Country.objects.all().count() - n} countries to db from pycountry. \n')


def load_currencies():
    currencies = pycountry.currencies
    n = Currency.objects.all().count()
    n_upd = 0
    for c in currencies:
        if Currency.objects.filter(symbol=c.alpha_3).exists():
            currency = Currency.objects.get(symbol=c.alpha_3)
            currency.name = c.name[:63]
            currency.save()
            n_upd += 1
        else:
            Currency.objects.create(name=c.name[:63], symbol=c.alpha_3)

    print(f'Added {Currency.objects.all().count() - n}  currencies to db. \n'
          f'Updated {n_upd}  currencies.')


def map_currencies():
    n = 0
    codes = {k: v[0] if v else None for k, v in country_currencies.CURRENCIES_BY_COUNTRY_CODE.items()}
    for country in Country.objects.all():
        try:
            code = codes[country.id]
            if Currency.objects.filter(symbol=code).exists():
                currency = Currency.objects.get(symbol=code)
                currency.issuer = country
                country.currency_code = code
                currency.save()
                country.save()
                n += 1
                print(f'Mapped {currency.name} ({currency.symbol}) to {country.name}')
        except Exception as e:
            print(f'Error: {e}')

    print(f'Mapped {n} currencies to countries.')



