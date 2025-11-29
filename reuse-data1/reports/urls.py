from django.contrib import admin
from django.urls import path


from . import views  ##importing the MM app view

urlpatterns = [
    path('materialflow/', views.materialflow, name='materialflow'),
    path('', views.materialflow, name='materialflow')
]
