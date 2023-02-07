from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *
from .markets_src import *
from website.models import *
from config import constants
from sqlalchemy import create_engine
from src.utils.formatting import color_cell2


class MarketsView(TemplateView):
    template_name = 'markets/markets.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = all_markets_data()
        context['currencies'] = constants.SORTED_CURRENCIES
        return context


class ForexView(TemplateView):
    template_name = 'markets/forex.html'

    def get_context_data(self, **kwargs):
        print(str(self.request.GET))
        if 'currency' in str(self.request.GET):
            currency = self.request.GET['currency']
        elif self.request.user.is_authenticated and Account.objects.get(user=self.request.user).currency.exists():
            currency = Account.objects.get(user=self.request.user).first().currency.symbol
        else:
            currency = constants.DEFAULT_CURRENCY
        rates_df = pd.DataFrame(get_fx_rates(currency))
        col_name = rates_df.columns[0]
        rates_df = rates_df[rates_df[col_name] != 1]
        rates = [(i, v[col_name]) for i, v in rates_df.iterrows()]

        currencies = list(rates_df.index.values)
        if currency in currencies:
            currencies.remove(currency)
        currencies.insert(0, currency)
        return {'currencies': currencies, 'rates': rates, 'add_ticker': Ticker()}



def forex_matrix(request):
    table = get_fx_rates(constants.DEFAULT_CURRENCY)
    context = {'currencies': constants.SORTED_CURRENCIES, 'table': table.to_html()}
    return render(request, 'markets/forex_matrix.html', context)


class IndicesView(TemplateView):
    template_name = 'markets/indices.html'


class ScreenerView(TemplateView):
    template_name = 'markets/screener.html'


class StocksView(TemplateView):
    template_name = 'markets/stocks.html'


class BondsView(TemplateView):
    template_name = 'markets/bonds.html'

class SectorsView(TemplateView):
    template_name = 'markets/sectors.html'

    def get_context_data(self, **kwargs):
        engine = create_engine(os.environ.get('LOCAL_DB_URL'))
        df = pd.read_sql('select * from markets.sectors', engine)
        df.drop('RT', 1, inplace=True)
        df.iloc[:,1:] = df.iloc[:,1:].applymap(color_cell2)
        return {'df': df.to_html(escape=False)}

class YieldCurvesView(TemplateView):
    template_name = 'markets/yield_curves.html'

    def get_context_data(self, **kwargs):
        if kwargs['country']:
            country = kwargs['country']
        else:
            country = 'United States'
        return {'main_curve': investpy.get_bonds_overview(country),
                'yield_curves': get_yield_curves()}


class CommoditiesView(TemplateView):
    template_name = 'markets/commodities.html'


class FundsView(TemplateView):
    template_name = 'markets/funds.html'


class ETFView(TemplateView):
    template_name = 'markets/etfs.html'


















