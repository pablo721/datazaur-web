from django.db import models


class Website(models.Model):
    title = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=128, blank=False)
    selectors = models.CharField(max_length=256, blank=True)


class Article(models.Model):
    url = models.CharField(max_length=128)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=512, blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=64, blank=True, null=True)
    tags = models.ManyToManyField('news.Tag')



class Tag(models.Model):
    text = models.CharField(max_length=32)




