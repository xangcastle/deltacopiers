

from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('moneycash.views',
    url(r'^$', index.as_view(), name='moneycash'),
    url(r'^factura/', factura.as_view(), name='moneycash_factura'),
    url(r'^roc/', roc.as_view(), name='moneycash_roc'),
    url(r'^bodega/', bodega.as_view(), name='moneycash_bodega'),
    url(r'^facturas_no_impresas/', facturas_no_impresas.as_view(),
        name='facturas_no_impresas'),
    url(r'^autocomplete_cliente/$', 'autocomplete_cliente',
        name='autocomplete_cliente'),
    url(r'^autocomplete_producto/$', 'autocomplete_producto',
        name='autocomplete_producto'),
    url(r'^detalle_producto/$', 'detalle_producto',
        name='detalle_producto'),
    url(r'^detalle_factura/$', 'detalle_factura',
        name='detalle_factura'),
    url(r'^grabar_factura/$', 'grabar_factura',
        name='grabar_factura'),
)
