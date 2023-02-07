import json
import yfinance
import os
import pandas as pd
import investpy
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.conf import settings
from django.views.generic import TemplateView

from markets.models import Stock
from db.load_fundamentals import profile_yahoo
from src.utils.charts import Chart
from src.utils.formatting import get_random_color
from datawarehouse.models import UpdateTime
from db.load_company_yahoo import save_company_to_db
from db.utils import camel_case_to_title
from .models import IncomeStatement, BalanceSheet, CashFlowStatement, Company, Recommendation




def search_companies(query):
    by_desc = Stock.objects.filter(description__icontains=query)
    by_symbol = Stock.objects.filter(displaySymbol__icontains=query)
    by_figi = Stock.objects.filter(figi__icontains=query)
    by_isin = Stock.objects.filter(isin__icontains=query)
    results = by_symbol.union(by_desc, by_figi, by_isin)
    return results


class BaseCompaniesView(TemplateView):
    template_name = 'companies/companies.html'
    def get_context_data(self, **kwargs):
        symbol = kwargs['symbol']


class SearchView(TemplateView):
    template_name = 'companies/companies.html'

    def get_context_data(self, **kwargs):
        results = {}
        if 'company_search_query' in str(self.request.GET):
            results = search_companies(self.request.GET['company_search_query'])
        return {'results': results}



class OverviewView(TemplateView):
    template_name = 'companies/overview.html'

    def get(self, request, *args, **kwargs):
        print('e;p2')
        print(request.GET)
        print(kwargs)
        if 'search' in str(request.GET) and request.is_ajax:
            results = search_companies(self.request.GET['company_search_input'])
            return render(request, 'companies/companies.html', {'results': results})

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        symbol = kwargs['symbol']
        SIDEBAR_ITEMS = [
            ['Overview', f'/companies/{symbol}/overview'],
            ['Market data', f'/companies/{symbol}/market_data'],
            ['Income statement', f'/companies/{symbol}/income_statement'],
            ['Balance sheet', f'/companies/{symbol}/balance_sheet'],
            ['Cashflow', f'/companies/{symbol}/cashflow'],
            ['Key metrics', f'/companies/{symbol}/key_metrics'],
            ['Ratios', f'/companies/{symbol}/ratios'],
            ['Insider trades', f'/companies/{symbol}/insider_trades'],
            ['Shareholders', f'/companies/{symbol}/shareholders'],
            ['Calendar', f'/companies/{symbol}/calendar'],
            ['News', f'/companies/{symbol}/news'],
            ['Recommendations', f'/companies/{symbol}/recommendations'],
            ['Analysis', f'/companies/{symbol}/analysis'],
            ['ESG', f'/companies/{symbol}/esg'],
        ]

        if UpdateTime.objects.filter(name=symbol).exists():
            last_upd = UpdateTime.objects.get(name=symbol).timestamp

        if not Company.objects.filter(symbol__iexact=symbol).exists():
            ticker = yfinance.Ticker(symbol)

            save_company_to_db(ticker)

        data = {}

        if Company.objects.filter(symbol__iexact=symbol).exists():
            data = Company.objects.get(symbol__iexact=symbol)

            # basic_data = data[:13]
            # market_data = data[13:20]
            # margins_data = data[20:24]
            # value_data = data[24:24]
            data = {camel_case_to_title(k): v for k, v in data.__dict__.items()}
            data.pop('_state')
            data.pop('Id')
            company_name = data.pop('Short Name')
            description = data.pop('Long Business Summary')
            logo_url = data.pop('Logo_url')
            website = data['Website']
            data['Website'] = f'<a href="{website}"> {website} </a>'

        return {'data': data, 'symbol': symbol, 'company_name': company_name, 'description': description,
               'logo_url': logo_url, 'sidebar_items': SIDEBAR_ITEMS}


class MarketDataView(TemplateView):
    template_name = 'companies/market_data.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'search_button' in str(request.GET) and request.is_ajax:
            results = search_companies(self.request.GET['company_search_input'])
            return render(request, 'companies/companies.html', {'results': results})

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        symbol = kwargs['symbol']

        period = self.request.GET['period'] if 'period' in str(self.request.GET) else '10y'
        ticker = profile_yahoo(symbol)
        interval = '5m' if period == '1d' else '1d'
        df = yfinance.download(symbol, period=period, interval=interval)
        df.loc[:, 'Symbol'] = ticker.ticker
        df.loc[:, 'Date'] = list(map(lambda x: int(x.timestamp() * 1000), df.index))
        company_name = ticker.info['shortName']
        df2 = df.loc[:, 'Date Open High Low Close'.split()]
        df2.loc[:, 'Date'] = df2.loc[:, 'Date'].astype('int64')
        df2.loc[:, 'Open High Low Close'.split()] = df2.loc[:, 'Open High Low Close'.split()].apply(lambda x: x.__round__(2))
        df2.columns = ["x", "o", "h", "l", "c"]
        data = [dict(row) for i, row in df2.iterrows()]
        context = {'symbol': symbol, 'company_name': company_name, 'data': data, 'start_date': str(df.index[0]),
                   'period': period}
        return context


class FinancialsView(TemplateView):
    template_name = 'companies/financials.html'

    def get_context_data(self, **kwargs):
        symbol = kwargs['symbol']
        return {'symbol': symbol}


class IncomeStatementView(FinancialsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = IncomeStatement.objects.filter()
        return context


class BalanceSheetView(FinancialsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['table'] = get_company_report(context['symbol'], 'balance_sheet', 'yahoo')
        return context


class CashFlowView(FinancialsView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['table'] = get_company_report(context['symbol'], 'cash_flow', 'yahoo')
        return context


class KeyMetricsView(TemplateView):
    template_name = 'companies/key_metrics.html'

    def get_context_data(self, **kwargs):
        return {}


class RatiosView(TemplateView):
    template_name = 'companies/ratios.html'

    def get_context_data(self, **kwargs):
        return {}


class InsiderSentimentView(TemplateView):
    template_name = 'companies/insider_sentiment.html'

    def get_context_data(self, **kwargs):
        return {}


class OptionsView(TemplateView):
    template_name = 'companies/options.html'

    def get_context_data(self, **kwargs):
        return {}


class OwnershipView(TemplateView):
    template_name = 'companies/ownership.html'

    def get_context_data(self, **kwargs):
        return {}


class RecommendationsView(TemplateView):
    template_name = 'companies/recommendations.html'

    def get_context_data(self, **kwargs):
        return {}


class RelatedNewsView(TemplateView):
    template_name = 'companies/related_news.html'

    def get_context_data(self, **kwargs):
        return {}


class EnterpriseValueView(TemplateView):
    template_name = 'companies/enterprise_value.html'

    def get_context_data(self, **kwargs):
        return {}



