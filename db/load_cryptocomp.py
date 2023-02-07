import pandas as pd
import json
import requests


class CryptocompareLoader:

    def __init__(self):
        pass

    def get_api_key(self):
        with open('secrets.json') as file:
            return json.load(file)['cryptocompare_api_key']

    def get_coins_info(self):
        api_key = self.get_api_key()
        url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={api_key}'
        data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Symbol', 'CoinName',
                                                                           'Description', 'Algorithm',
                                                                           'ProofType', 'TotalCoinsMined',
                                                                           'CirculatingSupply', 'MaxSupply',
                                                                           'BlockReward', 'AssetWebsiteUrl',
                                                                           'IsUsedInDefi', 'IsUsedInNft', 'BuiltOn',
                                                                           'SmartContractAddress']]

        return data

    def get_trading_signals(self, symbol):
        url = f'https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest?fsym={symbol}?api_key={self.api_key}'

        return pd.DataFrame(requests.get(url).json())
