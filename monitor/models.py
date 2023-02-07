from django.db import models


class InstrumentType:
    TYPES = enumerate(['cryptocurrency', 'stablecoin', 'currency', 'commodity', 'bond', 'stock', 'index'])
    CRYPTO = 'cryptocurrency'
    STABLECOIN = 'stablecoin'
    CURRENCY = 'currency'
    name = models.CharField(max_length=16)

class SourceType:
    TYPES = enumerate(['crypto_exchange', 'stock_exchange', 'data_provider', 'broker_dealer', 'trading_platform'])
    name = models.CharField(max_length=16)



class Watchlist(models.Model):
    owner = models.ForeignKey('website.Account', related_name='users_watchlists', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=32, default='Watchlist')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='watchlist_currency',
                                 blank=True, null=True)
    source = models.ForeignKey('crypto.CryptoExchange', on_delete=models.CASCADE, related_name='watchlist_source',
                                 blank=True, null=True)
    crypto_tickers = models.ManyToManyField('crypto.CryptoTicker', related_name='watchlist_crypto_tickers', blank=True)


#
# class Portfolio(Watchlist):
#     amounts = models.ManyToManyField('markets.Asset', related_name='portfolio_assets', blank=True,
#                                    through='watchlist.Amounts', through_fields=('portfolio', 'asset', 'amount', 'asset_class'))
#
#
#
# class Amounts(models.Model):
#     portfolio = models.OneToOneField('watchlist.Portfolio', on_delete=models.CASCADE, related_name='portfolio_crypto_amount')
#     asset = models.ForeignKey('markets.Asset', related_name='amounts_asset', blank=True, on_delete=models.CASCADE)
#     asset_class = models.CharField(max_length=32)
#     amount = models.FloatField(default=0)
#


