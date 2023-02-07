import yfinance
import pandas as pd
import datetime
import os
import sqlalchemy
from db.alchemy_utils import get_connection_string
from db.utils import camel_case_to_title
from datawarehouse.models import UpdateTime
from companies.models import Company, IncomeStatement, BalanceSheet, Recommendation, CashFlowStatement


def save_company_to_db(ticker):
    passwd = os.environ.get("LOCAL_DB_PASS")
    conn_string = get_connection_string('postgres', 'psycopg2', 'zaur', passwd, 'localhost', '5432', 'zaurdb2')
    overview = {camel_case_to_title(k): v for k, v in ticker.info.items()}

    print(overview)
    symbol = ticker.ticker

    for key in [
        'lastSplitDate',
        'lastDividendDate',
        'startDate',
    ]:
        try:
            ticker.info[key] = datetime.date.fromtimestamp(ticker.info[key])
        except:
            pass

    if 'Exchange' in overview.keys():
        exchange = overview['Exchange']
    else:
        exchange = 'NASDAQ'

    if not Company.objects.filter(symbol=symbol, exchange=exchange).exists():
        c = Company.objects.create(symbol=symbol, exchange=exchange)
        for k, v in ticker.info.items():
            print(k, v)
            c.__dict__[k] = v
            print(c.__dict__)
            c.save()

        print(f'Saved company {c.__dict__}')
        """
        income_statement = ticker.get_financials().transpose()
        for i, row in income_statement.iterrows():
            if not IncomeStatement.objects.filter(company=c, report_date=i).exists():
                print(row)
                row2 = {k: v.replace(' ', '_') for k, v in row.items()}
                row2.update({'company_id': c.id, 'report_date': i})
                IncomeStatement.objects.create(**row2)
                print(f'Income statement done for {c.symbol}')


        balance_sheet = ticker.get_balance_sheet().transpose()
        for i, row in balance_sheet.iterrows():
            if not BalanceSheet.objects.filter(company=c, report_date=i).exists():
                row2 = {k: v.replace(' ', '_') for k, v in row.items()}
                row2.update({'company_id': c.id, 'report_date': i})
                BalanceSheet.objects.create(**row2)
                print(f'Balance sheet done for {c.symbol}')

        cash_flow = ticker.get_cashflow().transpose()
        for i, row in cash_flow.iterrows():
            if not CashFlowStatement.objects.filter(company=c, report_date=i).exists():
                row2 = {k: v.replace(' ', '_') for k, v in row.items()}
                row2.update({'company_id': c.id, 'report_date': i})
                CashFlowStatement.objects.create(**row2)
                print(f'fCash flow done for {c.symbol}')

        #earnings_calendar = ticker.get_calendar()


        recommendations = ticker.get_recommendations()
        for i, row in recommendations.iterrows():
            if not Recommendation.objects.filter(company=c, report_date=i).exists():
                row2 = {k: v.replace(' ', '_') for k, v in row.items()}
                row2.update({'company_id': c.id, 'report_date': i})
                Recommendation.objects.create(**row2)
                print(f'Recomendations done for {c.symbol}')


    if not UpdateTime.objects.filter(name=symbol).exists():
        UpdateTime.objects.create(name=symbol, timestamp=datetime.datetime.now())
    else:
        upd = UpdateTime.objects.get(name=symbol)
        upd.timestamp = datetime.datetime.now()

    """

