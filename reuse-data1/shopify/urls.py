from django.contrib import admin
from django.urls import path



from shopify.views import *


urlpatterns = [
    path('acetap/', acetap, name='acetap'),
    path('lookup/', lookup, name='lookup'),
    path('queued/', queued, name='queued'),
    path('barcodetest/',barcodetest, name='barcodetest'),
    path('rchbarcodetest/',rchbarcodetest, name='rchbarcodetest'),
    path('rchbarcodesubmissiontest/',rchbarcodesubmissiontest, name='rchbarcodesubmissiontest'),
    path('rchpricingtest/', rchpricingtest, name='rchpricingtest'),
    path('rchpricing_usertest/', rchpricing_usertest, name='rchpricing_usertest'),
]
