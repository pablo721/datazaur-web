from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import TemplateView
from config import constants
from crypto.models import *
from .models import *
from .forms import *
from .utils import watchlist_prices
from markets.utils import get_currency
from markets.models import Ticker


class PortfolioView(TemplateView):
    template_name = 'monitor/portfolio.html'


class AlertsView(TemplateView):
    template_name = 'monitor/alerts.html'


class ScreenerView(TemplateView):
    template_name = 'monitor/screener.html'


class TwitterView(TemplateView):
    template_name = 'monitor/twitter.html'



class WatchlistView(TemplateView):
    template_name = 'monitor/watchlist.html'
    model = Watchlist
    forms = {'new_watchlist': NewWatchlist, 'add_coin': AddCoin, 'set_source': SetSource, 'select_source': SelectSource,
             'delete_watchlist': DeleteWatchlist, 'currency_form': ChangeCurrency}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)

        if not request.user.is_authenticated:
            return render(request, 'website/login_required.html')

        context = self.get_context_data(**kwargs)
        watchlist = context['watchlist']
        currency = watchlist.currency
        acc = request.user.user_account

        if 'watch_add_coin' in str(request.POST):
            print(request.POST)
            pk = request.POST['watch_add_coin_select']
            ticker = CryptoTicker.objects.get(pk=pk)
            #source = request.POST['source']
            #currency_code = get_currency(request).code



            if ticker not in watchlist.crypto_tickers.all():
                watchlist.crypto_tickers.add(ticker)
                watchlist.save()




        elif 'delete_from_watchlist' in str(request.POST):
            print(f'Start del from watchlist func')
            ticker_id = request.POST['checked_symbols']
            watchlist_id = request.POST['watchlist_id']
            if CryptoTicker.objects.filter(pk=ticker_id).exists() and Watchlist.objects.filter(pk=watchlist_id).exists():
                print(1)
                ticker = CryptoTicker.objects.get(pk=ticker_id)
                watchlist = Watchlist.objects.get(pk=watchlist_id)
                if ticker in watchlist.crypto_tickers.all() and watchlist.owner == acc:
                    print(2)
                    watchlist.crypto_tickers.remove(ticker)
                    watchlist.save()



        elif 'new_watch' in str(request.POST):
            watchlist_form = NewWatchlist(request.POST)
            if watchlist_form.is_valid():
                form_data = watchlist_form.cleaned_data
                form_data.update({'owner': request.user.user_account})
                form_data.update({'currency': Currency.objects.get(symbol=form_data['currency'])})
                form_data.update({'source': CryptoExchange.objects.get(pk=form_data['source'])})
                Watchlist.objects.create(**form_data)
            else:
                print(f'Errors: {watchlist_form.errors}')


        elif 'delete_watchlist' in str(request.POST):
            if Watchlist.objects.filter(id=kwargs['watchlist_id']).filter(owner=acc).exists():
                Watchlist.objects.filter(id=kwargs['watchlist_id']).filter(
                    owner=context['account']).first().delete()

        elif 'source' in str(request.POST):
            source_form = SetSource(request.POST)
            if source_form.is_valid():
                form_data = source_form.cleaned_data
                if CryptoExchange.objects.filter(name=form_data['exchange']).exists():
                    exchange = CryptoExchange.objects.get(name=form_data['exchange'])
                    if form_data['set_for_all']:
                        coins = watchlist.coins.all()
                    else:
                        coins = Cryptocurrency.objects.filter(symbol=form_data['coin'])
                    for coin in coins:
                        if Amounts.objects.filter(coin=coin).filter(watchlist=watchlist).exists():
                            p = Amounts.objects.filter(coin=coin).filter(watchlist=watchlist).first()
                            p.source = exchange
                            p.save()
                        else:
                            print(f'Errors: {source_form.errors}')

        elif 'currency' in str(request.POST):
            currency = Currency.objects.get(symbol=request.POST['currency'])
            watchlist.currency = currency
            watchlist.save()

        #import time
        #time.sleep(10)
        return HttpResponseRedirect(reverse('monitor:watchlist'))

    # def get_queryset(self, **kwargs):
    # 	if self.model.objects.filter(id=self.kwargs['watchlist_id']).filter(
    # 			owner=self.request.user_user_account).exists():
    # 		return self.model.objects.filter(id=self.kwargs['watchlist_id']).filter(
    # 			owner=self.request.user_user_account).first().coins().all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acc = self.request.user.user_account
        currency = Currency.objects.get(symbol='USD')
        source = CryptoExchange.objects.get(name='binance')


        if 'watchlist_id' in kwargs.keys() and Watchlist.objects.filter(id=kwargs['watchlist_id']).filter(
                owner=acc).exists():
            watchlist = Watchlist.objects.get(id=kwargs['watchlist_id'])
        elif acc.users_watchlists.exists():
            watchlist = acc.users_watchlists.first()
        else:
            watchlist = Watchlist.objects.create(owner=acc, name='Watchlist', currency=currency)
        if watchlist.currency:
            currency = watchlist.currency
        if watchlist.source:
            currency = watchlist.source

        context['account'] = acc
        context['watchlists'] = acc.users_watchlists.all()
        #context['currencies'] = constants.SORTED_CURRENCIES
        context['currency'] = currency
        context['coins'] = Cryptocurrency.objects.all()
        context['tickers'] = CryptoTicker.objects.all()
        context['watchlist'] = watchlist
        context['source'] = source
        context['watchlist_tickers'] = watchlist.crypto_tickers.all()

        context.update(self.forms)
        return context
