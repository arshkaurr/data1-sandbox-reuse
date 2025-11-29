from django.contrib import admin
from django.urls import path


from visitors.views import *

app_name='visitors'

urlpatterns = [

    path('submit/', submit, name='submit'),

    path('hourly/<slug:location>/', visitors_hourly, name='visitors_hourly'),
    path('<slug:location>/', VISITORS, name='VISITORS'),

    # path('capacity/', capacity, name='capacity'),


    # path('capacity_test/<slug:location>/', capacity_test, name='capacity_test'),
    # path('capacity_max_test/<slug:location>/', capacity_max_test, name='capacity_max_test'),


]
