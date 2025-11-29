"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


## This can be deleted later (this admin import)
from django.contrib import admin

from django.urls import path, include
from django.views.generic import TemplateView

from login.views import logout
from pricing.views import template_home



urlpatterns = [
    path('admin/', admin.site.urls), ## can be deleted later
    path('mm/',include('mm.urls')),
    path('idh/',include('idh.urls')),
    path('reports/',include('reports.urls')),
    path('shopify/', include('shopify.urls')),
    path('visitors/',include('visitors.urls')),
    path('pricing/', include('pricing.urls')),
    path('giftcardportal/', include('qbgiftcard.urls')),

    path('accounts/', include('allauth.urls')),

    path('', template_home, name='HOME'),
    # ORIGINAL BEFORE LINKS: path('', TemplateView.as_view(template_name='pricing/spark_base.html'), name='HOME'),
    path('logout/', logout)
]
