from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import django_filters.rest_framework as rest_filters

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from monitor.models import Watchlist
from crypto.models import CryptoTicker
from .serializers import WatchlistSerializer, CryptoTickerSerializer


class CryptoTickerViewSet(ModelViewSet):
    queryset = CryptoTicker.objects.all()
    serializer_class = CryptoTickerSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        serializer = CryptoTickerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, pk=pk)
        serializer = CryptoTickerSerializer(queryset)
        print(serializer.data)
        return Response(serializer.data)


class WatchlistViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]


    def list(self, request, *args, **kwargs):
        serializer = WatchlistSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = get_object_or_404(self.queryset, pk=pk)
        serializer = WatchlistSerializer(queryset)
        #print(serializer.data['crypto_tickers'])
        #serializer.data['crypto_tickers'] =  []#[[ticker.base, ticker.quote, ticker.source] for ticker in queryset.crypto_tickers.all()]
        #print(serializer.data['crypto_tickers'])
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print('pouut')