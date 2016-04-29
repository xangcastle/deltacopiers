# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('facturacion.views',
    url(r'^autocomplete_proveedor/$', 'autocomplete_proveedor',
        name='autocomplete_proveedor'),
    url(r'^autocomplete_producto/$', 'autocomplete_producto',
        name='autocomplete_producto'),
)
