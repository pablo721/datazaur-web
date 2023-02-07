from django.db import models


class MacroCalendar(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    zone = models.CharField(max_length=16, null=True, blank=True)
    currency = models.CharField(max_length=8, null=True, blank=True)
    importance = models.CharField(max_length=16, null=True, blank=True)
    event = models.CharField(max_length=128, null=True, blank=True)
    actual = models.CharField(max_length=16, null=True, blank=True)
    forecast = models.CharField(max_length=16, null=True, blank=True)
    previous = models.CharField(max_length=16, null=True, blank=True)


class CryptoCalendar(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    coins = models.CharField(max_length=256, null=True, blank=True)
    date_event = models.DateField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True)
    categories = models.CharField(max_length=256, null=True, blank=True)
    source = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['date_event']


class IPOCalendar(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    exchange = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    numberOfShares = models.FloatField(null=True, blank=True)
    price = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=32, null=True, blank=True)
    symbol = models.CharField(max_length=16, null=True, blank=True)
    totalSharesValue = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['date']


class EarningsCalendar(models.Model):
    id = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    reportDate = models.DateField(null=True, blank=True)
    fiscalDateEnding = models.DateField(null=True, blank=True)
    estimate = models.CharField(max_length=16, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        ordering = ['reportDate']



