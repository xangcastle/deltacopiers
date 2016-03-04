# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('facturacion.views',
    url(r'^autocomplete_cliente/$', 'autocomplete_cliente',
        name='autocomplete_cliente'),
    url(r'^autocomplete_producto/$', 'autocomplete_producto',
        name='autocomplete_producto'),
)
