import re
import pandas as pd
import os

from sqlalchemy import create_engine
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from src.utils.formatting import color_cell2, get_random_color
from datawarehouse.models import Config
from src.utils.charts import Chart
from markets.utils import get_currency, ordered_currencies, convert_fx
from website.models import Account
from markets.models import Currency, Commodity, Asset, Ticker
from macro.models import Country
from config import constants
from monitor.models import Watchlist
from .forms import *
from .models import *


# from .crypto_src import *


def crypto_change_currency(request):
    print(f'crypto chg curr post req: {request.POST}')
    try:
        acc = request.user.user_account
        acc.currency_code = request.POST['currency_code']
        acc.save()
        return redirect('crypto:crypto')

    except Exception as e:
        print(f'Couldnt change currency due to error: {e}')
        return HttpResponse(f'Couldnt change currency due to error: {e}')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class CryptoView(TemplateView):
    template_name = 'crypto/crypto.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'website/login_required.html')

        acc = request.user.user_account

        if is_ajax(request):
            if 'checked_symbols' in str(request.POST):
                print('ajax2')
                print(request.POST)
                symbols = request.POST['checked_symbols'].split(',')
                coin_ids = [symbol.split('_')[1].lower() for symbol in symbols if '_' in symbol]
                print(coin_ids)
                watchlist.coins.clear()
                for symbol in coin_ids:
                    watchlist.coins.add(Cryptocurrency.objects.filter(symbol=symbol).first())
                context['watchlist_ids'] = coin_ids

            elif 'new_currency' in str(request.POST):
                print(f'crypto view changing curr')
                print(request.POST)
                new_currency_code = request.POST['new_currency']
                if not Currency.objects.filter(code=new_currency_code).exists():
                    return HttpResponse('No such currency')
                else:
                    acc.currency_code = new_currency_code
                    acc.save()
                    return HttpResponseRedirect(reverse('crypto:crypto', args=()))


        elif 'amount' in str(request.POST):
            print('add to portfolio')
            print(request.POST)
            coin_id = request.POST['coin']
            new_amount = request.POST['amount']
            portfolio = Portfolio.objects.get(owner=account)
            if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id).exists():
                amount = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id)
                amount.amount += new_amount
                print(f'added {amount} to {coin_id}')
            else:
                amount = Amounts.objects.create(portfolio=portfolio, coin=coin_id, amount=new_amount)
                print(f'created {amount} of {coin_id}')
            amount.save()

        return HttpResponseRedirect(reverse('crypto:crypto', args=()))

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            account = self.request.user.user_account
        currency_code = account.currency_code if account.currency_code is not None else 'USD'
        currency = Currency.objects.get(symbol=currency_code)
        # print(f'crypto curr: {currency}')
        # print(f'users curr: {account.currency_code}')
        watchlists = []
        if self.request.user.is_authenticated:
            if Watchlist.objects.filter(owner=self.request.user.user_account).exists():
                watchlists = self.request.user.user_account.users_watchlists.all()

        account = self.request.user.user_account
        currencies = Currency.objects.all()
        countries = Country.objects.all()
        watchlist = Watchlist.objects.filter(owner=account).first()
        watchlist_tickers = watchlist.crypto_tickers.all()
        watchlist_ids = [c.base for c in watchlist_tickers]
        url = os.environ.get('LOCAL_DB_URL')
        engine = create_engine(url)
        table = pd.read_sql('top_coins', engine)

        cols = [table.columns[n] for n in [2, 5, 6]]

        if currency_code != 'USD':
            print(f'table currL {table.currency} user curr: {currency_code}')
            print(table)
            table = convert_fx(table, cols, table.currency, currency_code)
            print('converted')
            print(table)

        table['Watchlist'] = table['Symbol'].apply(lambda
                                                       x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x}" value="{x}" class="star">""")
        table['Portfolio'] = table['Symbol'].apply(lambda
                                                       x: f""" <button type="submit" name="add_to_pf" value="{x}"> Add </button>""")
        table.drop(labels=['index', 'Url'], axis=1, inplace=True)
        # table[['Price', '1h Δ', '24h Δ']] = table[['Price', '1h Δ', '24h Δ']].apply(lambda x: )
        table = table.to_html(escape=False, justify='center')

        return {'currency': currency, 'currencies': currencies, 'countries': countries, 'tickers': watchlist_tickers,
                'watchlists': watchlists, 'watchlist_ids': watchlist_ids, 'table': table}


# table['Watchlist'] = table['Symbol'].apply(lambda
#                                                x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x.split('</a>')[0].split('>')[1]}" class="star">""")
# table['Portfolio'] = table['Symbol'].apply(lambda
#                                                x: f""" <button type="submit" name="add_to_pf" value="{x.split('</a>')[0].split('>')[1]}"> Add </button>""")

def crypto(request):
    context = {}
    context['currencies'] = Currency.objects.all()

    coin_ids = []

    table = top_coins_by_mcap()
    table['Watchlist'] = table['Symbol'].apply(lambda
                                                   x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x.split('</a>')[0].split('>')[1]}" class="star">""")
    table['Portfolio'] = table['Symbol'].apply(lambda
                                                   x: f""" <button type="submit" name="add_to_pf" value="{x.split('</a>')[0].split('>')[1]}"> Add </button>""")
    context['table'] = table.to_html(escape=False, justify='center')

    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        watchlist = Watchlist.objects.filter(user=account).first()
        coins = watchlist.coins.all()

        print(coins)
        context['watchlist_ids'] = [c.symbol.lower() for c in coins]
        print(context['watchlist_ids'])
        if account.currency:
            context['currency'] = account.currency.symbol
        else:
            context['currency'] = constants.DEFAULT_CURRENCY

    if request.method == 'GET':
        return render(request, 'crypto/crypto_calendar.html', context)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'website/login_required.html', context)

        elif request.is_ajax and 'checked_symbols' in str(request.POST):
            print('ajax2')
            print(request.POST)
            symbols = request.POST['checked_symbols'].split(',')
            coin_ids = [symbol.split('_')[1].lower() for symbol in symbols if '_' in symbol]
            print(coin_ids)
            watchlist.coins.clear()
            for symbol in coin_ids:
                watchlist.coins.add(Cryptocurrency.objects.filter(symbol=symbol).first())
            context['watchlist_ids'] = coin_ids

        elif 'amount' in str(request.POST):
            print('add to portfolio')
            print(request.POST)
            coin_id = request.POST['coin']
            new_amount = request.POST['amount']
            portfolio = Portfolio.objects.get(user=account)
            if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id).exists():
                amount = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id)
                amount.amount += new_amount
                print(f'added {amount} to {coin_id}')
            else:
                amount = Amounts.objects.create(portfolio=portfolio, coin=coin_id, amount=new_amount)
                print(f'created {amount} of {coin_id}')
            amount.save()

        return HttpResponseRedirect(reverse('crypto:crypto', args=()))


def add_exchange(request):
    exchange_id = request.POST['exchange_id']
    value = request.POST['value']
    print(value)
    user = request.user.profile
    exchange = Exchange.objects.get(id=exchange_id)
    if value:
        user.exchanges.add(exchange)
        msg = 'added'
    else:
        user.exchanges.remove(exchange)
        msg = 'removed'
    return HttpResponse(msg)


class ExchangesView(ListView):
    template_name = 'crypto/exchanges.html'
    model = CryptoExchange

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favourites'] = [exchange.id for exchange in self.request.user.user_account.exchanges.all()]
        print(context)
        return context


class DominanceView(DetailView):
    template_name = 'crypto/dominance.html'

    top_n_choices = [10, 20, 50, 100]
    mcap_col = f'Market cap (USD)'

    def get_queryset(self):
        return Cryptocurrency.objects.filter(price > 0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
        top_n_choices.remove(top_n_coins)
        top_n_choices.insert(0, top_n_coins)
        PALETTE = [get_random_color() for i in range(top_n_coins)]
        df = pd.read_csv('crypto.files', index_col=0).iloc[:top_n_coins][['Symbol', mcap_col]]
        df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
        df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
        # df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
        chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
        chart.from_df(df, values='Dominance', labels=list(df.loc[:, 'Symbol']))
        js_scripts = chart.get_js()
        context['charts'] = []
        context['charts'].append(chart.get_presentation())
        context['table'] = chart.get_html()
        context['js_scripts'] = js_scripts
        context['top_n_choices'] = top_n_choices
        return context


def dominance(request):
    db_url = os.environ.get('LOCAL_DB_URL')
    engine = create_engine(db_url)
    context = {}
    if request.user.is_authenticated:
        acc = Account.objects.get(user=request.user)
        if acc.currency_code:
            currency = acc.currency_code
    else:
        currency = DEFAULT_CURRENCY
    top_n_choices = [10, 20, 50, 100]
    mcap_col = f'Market cap (USD)'

    if request.method == 'GET':
        top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
        top_n_choices.remove(top_n_coins)
        top_n_choices.insert(0, top_n_coins)
        PALETTE = [get_random_color() for i in range(top_n_coins)]
        df = pd.read_sql('select * from public.crypto_dominance;', engine)  # .iloc[:top_n_coins][['Symbol', mcap_col]]
        df['index'] = df['index'].apply(lambda x: x.upper())
        # df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
        # df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
        # df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
        chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
        chart.from_df(df, values='market_cap_percentage', labels=list(df.loc[:, 'index']))
        js_scripts = chart.get_js()
        # context['chart'] = []
        # context['charts'].append(chart.get_presentation())
        context['chart'] = chart.get_html()
        table = df.loc[:, ['index', 'market_cap_percentage']]
        table.columns = ['coin', 'dominance']
        table['dominance'] = table['dominance'].apply(lambda x: str(x.__round__(2)) + '%')
        context['table'] = table.to_html(escape=False)
        context['js_scripts'] = js_scripts
        context['top_n_choices'] = top_n_choices

        return render(request, 'crypto/dominance.html', context)


class GlobalMetricsView(TemplateView):
    template_name = 'crypto/global_metrics.html'

    def get_context_data(self, **kwargs):
        db_url = os.environ.get('LOCAL_DB_URL')
        engine = create_engine(db_url)
        with engine.connect() as conn:
            df_metrics = pd.read_sql('select * from public.crypto_metrics', conn).iloc[:, 1:].to_html(escape=False)

        return {'metrics': df_metrics}


class NFTView(TemplateView):
    template_name = 'crypto/nft.html'


class DeFiView(TemplateView):
    template_name = 'crypto/defi.html'


class MoversView(TemplateView):
    template_name = 'crypto/movers.html'

    def get_context_data(self, **kwargs):
        gainers = CryptoTicker.objects.all().order_by('-daily_delta')[:20].values()
        losers = CryptoTicker.objects.all().order_by('daily_delta')[:20].values()
        gainers_df = pd.DataFrame(gainers).dropna(subset='daily_delta').loc[:,
                     ['base', 'quote', 'price', 'daily_delta', 'timestamp', 'source']]
        losers_df = pd.DataFrame(losers).dropna(subset='daily_delta').loc[:,
                    ['base', 'quote', 'price', 'daily_delta', 'timestamp', 'source']]
        gainers_df['daily_delta'] = gainers_df['daily_delta'].apply(color_cell2)
        losers_df['daily_delta'] = losers_df['daily_delta'].apply(color_cell2)
        gainers_df['timestamp'] = gainers_df['timestamp'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%m'))
        losers_df['timestamp'] = losers_df['timestamp'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%m'))
        gainers_df['base'] = gainers_df['base'] + '/' + gainers_df['quote']
        losers_df['base'] = losers_df['base'] + '/' + losers_df['quote']
        gainers_df = gainers_df.rename(mapper={'base': 'ticker'}, axis=1).drop('quote', axis=1).to_html(escape=False)
        losers_df = losers_df.rename(mapper={'base': 'ticker'}, axis=1).drop('quote', axis=1).to_html(escape=False)
        return {'gainers': gainers_df,
                'losers': losers_df}
