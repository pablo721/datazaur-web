import pandas as pd
from pycoingecko import CoinGeckoAPI
import json


class GeckoLoader:

    def __init__(self):
        self.client = CoinGeckoAPI()

    def get_secret(self, key):
        with open('secrets.json') as file:
            return json.loads(file.read())[key]

    def load_exchanges(self):
        return pd.DataFrame(self.client.get_exchanges_list())

    def load_defi(self):
        url = 'https://api.coingecko.com/api/v3/global/decentralized_finance_defi'
        return pd.DataFrame(json.loads(requests.get(url).text))


    def load_crypto_indexes(self):
        return pd.DataFrame(self.client.get_indexes())

    def load_gecko_coins(self):
        return pd.DataFrame(self.client.get_coins_list())

    def load_derivatives(self):
        return pd.DataFrame(self.client.get_derivatives())

    def load_derivatives_exchanges(self):
        return pd.DataFrame(self.client.get_derivatives_exchanges())

    def load_global_metrics(self):
        df = pd.DataFrame(self.client.get_global())[['market_cap_percentage']]
        df['name'] = df.index
        df.dropna(subset='market_cap_percentage', inplace=True)
        return df.sort_values(by='market_cap_percentage', ascending=False)

    def load_coin_categories(self):
        return pd.DataFrame(self.client.get_coins_categories_list())

    def load_public_companies_coin_holdings(self, coin_id='BTC'):
        return pd.DataFrame(self.client.get_companies_public_treasury_by_coin_id(coin_id))


