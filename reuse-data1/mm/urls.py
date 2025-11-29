from django.contrib import admin
from django.urls import path


from mm.views import *  ##importing the MM app view

app_name='mm'

urlpatterns = [
    path('', mm, name='mm'), ## can be deleted later
    path('submit/', mmsubmit,name='mmsubmit'),
    path('rawdata/', rawdata, name='rawdata'),
    path('movement/', movement, name='movement'),
    path('movement_submit/', movement_submit, name='movement_submit'),

    path('stats/<slug:location>/', stats_location, name='stats_location'),

    path('stats/', stats, name='stats' ),
    path('raw/', raw, name='raw'),




]
