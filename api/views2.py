from django.http import JsonResponse
import django_filters.rest_framework as rest_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from markets.models import Ticker, Currency, Commodity, Asset
from crypto.models import Cryptocurrency
from macro.models import Country
from monitor.models import *
from calendar_.models import MacroCalendar, CryptoCalendar





class CryptoView(ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptoSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]

    def get_queryset(self):
        return JsonResponse({'a': 1})




# class PortfolioView(viewsets.ModelViewSet):
# 	queryset = Portfolio.objects.all()
# 	serializer_class = PortfolioSerializer


class CurrencyView(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CountryView(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CommodityView(ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


class MacroCalendarView(ModelViewSet):
    queryset = MacroCalendar.objects.all()
    serializer_class = MacroCalendarSerializer


class CryptoCalendarView(ModelViewSet):
    queryset = CryptoCalendar.objects.all()
    serializer_class = CryptoCalendarSerializer
