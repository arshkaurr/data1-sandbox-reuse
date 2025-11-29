from django.db import models

# Create your models here.
class GiftCard(models.Model):
    first_name = models.CharField(max_length = 128, default='', blank=True)
    last_name = models.CharField(max_length = 128, default='', blank=True)
    phone = models.CharField(max_length = 16, default='', blank=True)
    email = models.CharField(max_length = 256, default='', blank=True)
    giftcard = models.CharField(max_length = 256, default='')
    initial_balance = models.DecimalField(max_digits = 6, decimal_places = 2, default = '0.0')

    STATUS_CHOICES = (('i','initial'),('q','qbgiftcard'),('u','upgraded'),('r','remap'))
    status = models.CharField(default = 'i', max_length = 1, choices = STATUS_CHOICES)

    timestamp_created = models.DateTimeField(auto_now_add = True)
    timestamp_updated = models.DateTimeField(auto_now = True)

    UID = models.IntegerField(default=-1)
    LINK = models.CharField(max_length = 129, default='')


    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class AccessLog(models.Model):
    staff_id = models.CharField(max_length = 32)
    giftcard = models.ForeignKey(GiftCard, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.staff_id}, {self.timestamp}'
