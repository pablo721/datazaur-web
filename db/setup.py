import datetime
import time
import os
from sqlalchemy import create_engine
from .load_calendars import CalendarLoader
from .load_countries import load_currencies, map_currencies
from .load_pd import wb_countries, wb_sources, wb_regions, wb_lendingtypes, wb_incomelevels, wb_topics, wb_indicators
from .load_stocks import load_exchanges, load_stocks_finnhub
from .load_markets2 import MarketsLoader
from .load_crypto2 import load_all_crypto
from .load_config2 import load_config
from .load_gecko import GeckoLoader
from .load_ccxt import CCXTLoader
from .load_cryptocomp import CryptocompareLoader
from .db_client import BaseDbClient




def setup_all():
    create_schemas()
    url = os.environ.get('LOCAL_DB_URL')
    db_client = BaseDbClient(url)
    markets_loader = MarketsLoader(url)
    markets_loader.load_all_markets()

    calendar_loader = CalendarLoader(url)
    calendars = calendar_loader.load_all_calendars()

    print(f'Starting calendars')
    for key, df in calendars.items():
        db_client.save_df_to_db(df, key + '_calendar', 'calendar', 'replace')
    print(f'Done calendars')

    # print(f'Starting CCXT')
    # ccxt_loader = CCXTLoader()
    #
    # for func in [ccxt_loader.load_crypto_tickers]:
    #     df = func()
    #     db_client.save_df_to_db(df, func.__name__.replace('load_', ''), 'monitor', 'replace')
    # print(f'Done CCXT')

    print(f'Start config')
    load_config(url)
    print(f'Done config')

    print(f'Start crypto')
    load_all_crypto()
    print(f'Done crypto')

    print(f'Start WB')
    setup_wb()
    print(f'Done WB')

def create_schemas():
    schemas = ['config', 'crypto', 'markets', 'macro', 'monitor', 'calendar', 'temp']
    url = os.environ.get('LOCAL_DB_URL')
    engine = create_engine(url, echo=True)
    with engine.connect() as conn:
        for schema in schemas:
            try:
                conn.execute(f'create schema {schema}; grant all on schema {schema} to zaur;')
            except Exception as e:
                print(f'Error {e} when creating  schema {schema}')


def setup_wb():
    setup_funcs2 = [wb_countries, wb_sources, wb_regions, wb_topics, wb_lendingtypes, wb_incomelevels, wb_indicators,
                    load_currencies, map_currencies]
    success = []
    errors = []
    for func in setup_funcs2:
        try:
            t = datetime.datetime.now().timestamp()
            print(f'Starting {func.__name__}')
            func()
            print(f'Function {func.__name__} executed successfully in {datetime.datetime.now().timestamp() - t} seconds.')
            success.append(func.__name__)
        except Exception as e:
            print(f'Error {e} while executing function {func.__name__}.')
            errors.append([func.__name__, e])
        finally:
            time.sleep(1)

    print(f'Successes: {success} \nFailures: {errors}')
    return success, errors


