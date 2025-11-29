from django.db import models

# Create your models here.


class Visitors(models.Model):
    timestamp = models.DateTimeField()
    count = models.IntegerField()
    location = models.CharField(max_length=64)
    capacity = models.FloatField(null=True)

class Site(models.Model):
    location = models.CharField(max_length=64)
    capacity = models.IntegerField()
