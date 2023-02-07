from sqlalchemy import create_engine
import pandas as pd
import os
import datetime
import requests
import investpy
import pandas_datareader.data as web
from forex_python.converter import CurrencyRates
from config import constants


class MarketsLoader:
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(url)
        self.schema = 'markets'

    def save_to_db(self, df, table_name, if_exists, index=False):
        df.to_sql(table_name, self.engine, self.schema, if_exists, index)
        print(f'Loaded {table_name}.')


    def load_all_markets(self):
        try:
            self.engine.execute('create schema markets;')
        except:
            pass
        dfs = {}
        dfs['crypto'] = self.load_crypto()
        dfs['fx_rates'] = self.load_fx()
        dfs['fx_crosses'] = self.load_currency_crosses()
        dfs['indices'] = self.load_indices()
        dfs['bonds'] = self.load_bonds()
        dfs['commodities'] = self.load_commodities()
        dfs['commodities_data'] = self.load_commodities_data()
        dfs['sectors'] = self.load_sectors()
        print(dfs)

        for key, df in dfs.items():
            try:
                self.save_to_db(df, key, if_exists='replace', index=False)
            except Exception as e:
                print(f'Exception: {e}')


    def load_crypto(self, currency='USD'):
        api_key = os.environ.get('CRYPTOCOMPARE_API_KEY')
        url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=50&tsym={currency}&api_key={api_key}'
        cols = f'CoinInfo.Name RAW.{currency}.PRICE RAW.{currency}.CHANGE24HOUR RAW.{currency}.CHANGEPCT24HOUR'.split()
        df = pd.json_normalize(requests.get(url).json()['Data'])[cols]
        df.columns = ['Symbol', 'Price', '24h Δ', '24h %Δ']
        return df


    def load_fx(self, currency='USD'):
        rates = CurrencyRates()
        rates_df = pd.DataFrame(pd.Series(rates.get_rates(currency))).reset_index(drop=False)
        rates_df['quote'] = currency
        rates_df.columns = ['base', 'price', 'quote']
        return rates_df



    def load_currency_crosses(self, currency='USD'):
        return investpy.get_currency_crosses(currency)

    def load_indices(self):
        indices = constants.STOCK_INDICES
        result = pd.DataFrame(columns=['Index', 'Price', '24h Δ', '24h %Δ'])
        for k, v in indices.items():
            for indx in v:
                try:
                    df = investpy.get_index_recent_data(indx, k)['Close'].iloc[-2:]
                    diff = (df[1] - df[0]).__round__(2)
                    diff_pct = (100 * diff / df[0]).__round__(2)
                    result.loc[len(result)] = {'Index': f"""{indx} <br> ({k.title()})""",
                                               'Price': df[1],
                                               '24h Δ': diff,
                                               '24h %Δ': diff_pct}

                except Exception as e:
                    print(f'error {e}')

        result.iloc[:, 1] = result.iloc[:, 1].astype(float).round(2)
        return result


    def load_bonds(self, tenor='10Y'):
        result = pd.DataFrame(columns=['Bond', 'Yield', '24h Δ', '24h %Δ'])
        today = datetime.date.today()
        n_days_diff = self.find_days_diff(today)
        start_date = today - datetime.timedelta(days=n_days_diff)
        end_date = today - datetime.timedelta(days=n_days_diff - 1)
        start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%d/%m/%Y")
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%d/%m/%Y")
        if 'yields.files' in os.listdir():
            countries = [bond.split(' 10')[0] for bond in pd.read_csv('yields.files', index_col=0)['Bond']]
        else:
            countries = investpy.get_bond_countries()
        for country in countries:
            bond = country + ' ' + tenor
            try:
                data = investpy.get_bond_historical_data(f'{bond}', from_date=start_date, to_date=end_date).iloc[-2:]
                diff = data['Close'].iloc[1] - data['Close'].iloc[0]
                diff_pct = 100 * diff / data['Close'].iloc[0]
                result.loc[len(result)] = [bond.title(), data['Close'].iloc[-1], diff, diff_pct]
            except Exception as e:
                print(f'error {e}')

        return result

    def load_commodities_data(self):
        cols = ['title', 'country', 'name', 'full_name', 'currency', 'group']
        res = pd.DataFrame(columns=cols)
        groups = investpy.get_commodity_groups()
        for group in groups:
            try:
                df = investpy.get_commodities(group)[cols]
                df['group'] = group
                df.name = group
                res = pd.concat([res, df])
            except Exception as e:
                print(f'Exception: {e}')
        return res

    def load_commodities(self):
        cols = ['name', 'country', 'last', 'change', 'change_percentage', 'currency']
        res = pd.DataFrame(columns=cols)
        result_cols = ['Instrument', 'Price', '24h Δ', '24h %Δ']
        groups = investpy.get_commodity_groups()
        for group in groups:
            try:
                df = investpy.get_commodities_overview(group)[cols]
                df['group'] = group
                df.name = group
                res = res.append(df)
            except Exception as e:
                print(f'Exception: {e}')
        return res

    def load_sectors(self):
        key = os.environ.get('ALPHAVANTAGE_API_KEY')
        df = web.get_sector_performance_av(api_key=key)
        df = df.applymap(lambda x: str(x).replace('%', ''))
        cols = df.columns[1:]
        df[cols] = df[cols].astype('float64')
        return df.reset_index(drop=False)


    @staticmethod
    def find_days_diff(today):
        if today.isoweekday() == 6:
            return 2
        elif today.isoweekday() == 7:
            return 3
        elif today.isoweekday() == 1:
            return 4
        else:
            return 1

