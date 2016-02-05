# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('moneycash.contabilidad.views',
    url(r'^contabilidad/comprobante/(?P<id>.*)/$',
        'imprimir_comprobante', name='imprimir_comprobante'),)
