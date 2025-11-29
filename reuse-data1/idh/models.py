from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ddo_hourly(models.Model):
    hDate = models.DateField()
    h08 = models.IntegerField()
    h09 = models.IntegerField()
    h10 = models.IntegerField()
    h11 = models.IntegerField()
    h12 = models.IntegerField()
    h13 = models.IntegerField()
    h14 = models.IntegerField()
    h15 = models.IntegerField()
    h16 = models.IntegerField()
    h17 = models.IntegerField()
    h18 = models.IntegerField()
    h19 = models.IntegerField()
    hTotal = models.IntegerField(default=-1)
    def __str__(self):
        return str(self.hDate)
