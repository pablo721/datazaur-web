from rest_framework import serializers
from markets.models import Ticker, Asset, Commodity, Currency
from macro.models import Country
from crypto.models import CryptoExchange, Cryptocurrency, CryptoTicker
from monitor.models import *
from calendar_.models import MacroCalendar, CryptoCalendar

class CryptoExchangeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    url = serializers.StringRelatedField()
    class Meta:
        model = CryptoExchange
        fields = ['name', 'url']

class CryptoTickerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    base = serializers.StringRelatedField()
    quote = serializers.StringRelatedField()
    source = serializers.StringRelatedField()
    class Meta:
        model = CryptoTicker
        fields = ['id', 'base', 'quote', 'source', 'price', 'bid', 'ask', 'timestamp']


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'owner', 'currency', 'source', 'crypto_tickers', 'add_tickers', 'remove_tickers']
        #depth = 1
        extra_kwargs = {
            'name': {'validators': []},  # remove uniqueness validation
        }

    owner = serializers.StringRelatedField(required=False)
    #source = serializers.StringRelatedField(required=False)
    crypto_tickers = CryptoTickerSerializer(many=True, required=False)
    add_tickers = CryptoTickerSerializer(many=True, required=False)
    remove_tickers = CryptoTickerSerializer(many=True, required=False)


    def update(self, instance, validated_data):
        print('upd')
        print(validated_data)
        if 'add_tickers' in validated_data.keys():
            ticks = validated_data.pop('add_tickers')[0]
            for k, v in ticks.items():
                instance.crypto_tickers.add(v)

        if 'remove_tickers' in validated_data.keys():
            ticks = validated_data.pop('remove_tickers')[0]
            for k, v in ticks.items():
                instance.crypto_tickers.remove(v)

        print(validated_data)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance




class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['name', 'symbol', 'asset_class']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'code', 'issuer']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'countries']


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name', 'symbol', 'group']


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = ['url']


class CryptoExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoExchange
        fields = ['symbol', 'name', 'url']



# class PortfolioSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Portfolio
# 		fields = ['name', 'owner', 'currency', 'assets', 'private', 'creation_date']


class MacroCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MacroCalendar
        fields = ['name']


class CryptoCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCalendar
        fields = ['name']


