from django.db import models
from config import constants


class CryptoExchange(models.Model):
    name = models.CharField(max_length=128)
    grade = models.CharField(choices=enumerate(constants.CRYPTO_EXCHANGE_GRADES), max_length=3, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    countries = models.ManyToManyField('macro.Country', related_name='cryptoexchange_countries')
    currencies = models.ManyToManyField('markets.Currency', related_name='cryptoexchange_currencies')
    tickers = models.ManyToManyField('markets.Ticker', related_name='cryptoexchange_tickers')
    daily_vol = models.FloatField(null=True, blank=True)
    monthly_vol = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    symbol = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    hash_algorithm = models.CharField(max_length=64, null=True, blank=True)
    proof_type = models.CharField(max_length=32, null=True, blank=True)


class CryptoTicker(models.Model):
    base = models.CharField(max_length=16)
    quote = models.CharField(max_length=16)
    price = models.FloatField(null=True)
    bid = models.FloatField(null=True)
    ask = models.FloatField(null=True)
    hourly_delta = models.FloatField(null=True)
    daily_delta = models.FloatField(null=True)
    weekly_delta = models.FloatField(null=True)
    monthly_delta = models.FloatField(null=True)
    timestamp = models.DateTimeField(null=True)
    source = models.CharField(max_length=32)


    def __str__(self):
        return f'{self.base}/{self.quote}: {self.price} - {self.source}'

    class Meta:
        #managed = False
        #db_table = 'monitor_cryptoticker'
        unique_together = (('base', 'quote', 'source'),)

