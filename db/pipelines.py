import datetime

from sqlalchemy import insert, create_engine
from sqlalchemy.orm import Session

from .alchemy_models import Log
from load_pd import wb_regions, wb_lendingtypes, wb_incomelevels, wb_sources, wb_countries
from .load_stocks import load_exchanges, load_stocks_finnhub
from .load_news import load_crypto_news, crypto_news_feed, load_finnhub_news
from .load_crypto import load_cryptocomp_coins, load_crypto_exchanges, load_crypto_tickers




def run_pipeline(funcs, rollback_on_fail=True):
    engine = create_engine('postgresql+psycopg2://zaur:wsad1221@localhost:5432/zaurdb2')
    session = Session(engine)
    for func in funcs:
        func_name = func.__name__
        print(f'Starting {func_name}')
        t = datetime.datetime.now().timestamp()
        log = [t, func_name]
        try:
            func()
            print(f'Function {func_name} executed successfully in {datetime.datetime.now().timestamp() - t} seconds.')
            log += [f'Function {func_name} executed successfully in {datetime.datetime.now().timestamp() - t} seconds.', 0]
            session.execute(insert(Log).values(log))
        except Exception as e:
            print(f'Error {e}')
            if rollback_on_fail:
                log += [f'Error {e} \nRolling back changes.', 1]
                session.rollback()
                session.execute(insert(Log).values(log))
                session.commit()
                return 1
    session.commit()
    return 0





pipeline_wb =[
    wb_regions,
    wb_lendingtypes,
    wb_incomelevels,
    wb_sources,
    wb_countries
]





pipeline_wb2 = ['wb_topics', 'wb_indicators']


def pipeline_stocks():
    load_exchanges()
    load_stocks_finnhub()


def pipeline_news():
    load_finnhub_news()
    load_crypto_news()
    crypto_news_feed()


def pipeline_crypto():
    load_crypto_exchanges()
    load_cryptocomp_coins()
    load_crypto_tickers()



