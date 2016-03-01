# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='moneycash'),
    url(r'^facturacion/$', FacturacionPage.as_view(), name='facturacion'),
    url(r'^register_empresa/$', 'moneycash.views.register_empresa',
        name='moneycash_register_empresa'),
]
