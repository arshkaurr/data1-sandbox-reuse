from django.urls import path

from qbgiftcard.views import *

app_name='qbgiftcard'

urlpatterns = [
    path('', qbgiftcardhome, name='qbgiftcardhome'),

    path('results/', results, name='results'),

    path('lookup/', lookup, name='lookup'),

    # path('printlabel', printlabel, name='printlabel')

]
