from django.db import models


class DataCategory(models.Model):
    CHOICES = []
    category_name = models.CharField(max_length=64)





class Dataset(models.Model):
    source = models.CharField(max_length=64)
    database_code = models.ForeignKey('datawarehouse.Database', on_delete=models.CASCADE, related_name='database_datasets')
    dataset_code = models.CharField(max_length=128)
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    frequency = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.database_code + '/' + self.dataset_code


class Config(models.Model):
    key = models.CharField(max_length=64, unique=True, null=False, blank=False)
    value = models.CharField(max_length=256)


# status 0 - executed correctly; 1 - error
class Log(models.Model):
    source = models.CharField(max_length=64)
    timestamp = models.DateTimeField()
    status = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=512, blank=True, null=True)


class Source(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=256, blank=True, null=True)


class Endpoint(models.Model):
    source = models.ForeignKey('datawarehouse.Source', on_delete=models.CASCADE, related_name='source_endpoints')
    url = models.CharField(max_length=256)


class Database(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, null=True, blank=True)
    database_code = models.CharField(max_length=128, primary_key=True)


class UpdateTime(models.Model):
    name = models.CharField(max_length=64, unique=True)
    timestamp = models.DateTimeField()













