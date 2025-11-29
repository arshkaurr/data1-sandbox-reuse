from django.contrib import admin
from django.urls import path


from . import views  ##importing the MM app view

urlpatterns = [
    path('', views.idh, name='idh'), ## can be deleted later
]
