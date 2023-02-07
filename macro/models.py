from django.db import models




class Country(models.Model):
    iso3c = models.CharField(max_length=3)
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=128)
    region = models.CharField(max_length=64, null=True, blank=True)
    adminregion = models.CharField(max_length=64, null=True, blank=True)
    incomeLevel = models.CharField(max_length=64, null=True, blank=True)
    lendingType = models.CharField(max_length=64, null=True, blank=True)
    capitalCity = models.CharField(max_length=128)
    longitude = models.FloatField()
    latitude = models.FloatField()
    currency_code = models.CharField(max_length=3, null=True, blank=True)




class Region(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    iso2code = models.CharField(max_length=2)
    name = models.CharField(max_length=64)


class WBSource(models.Model):
    id = models.IntegerField(primary_key=True)
    lastupdated = models.DateTimeField()
    name = models.CharField(max_length=70)
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=128, null=True, blank=True)


class WBTopic(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=70)
    sourceNote = models.CharField(max_length=1024)


class WBIncomeLevel(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    iso2code = models.CharField(max_length=2)
    value = models.CharField(max_length=21)


class WBLendingType(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    iso2code = models.CharField(max_length=2)
    value = models.CharField(max_length=21)


class WBIndicator(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=16, null=True, blank=True)
    source = models.CharField(max_length=128, null=True, blank=True)
    sourceNote = models.CharField(max_length=512)
    sourceOrganization = models.CharField(max_length=256)
    topics = models.ManyToManyField('macro.WBTopic')


