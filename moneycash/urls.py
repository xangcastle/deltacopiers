

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
    url(r'^extract_cliente/$', 'extract_cliente',
        name='extract_cliente'),
    url(r'^detalle_cliente/$', 'detalle_cliente',
        name='detalle_cliente'),
    url(r'^detalle_factura/$', 'detalle_factura',
        name='detalle_factura'),
    url(r'^grabar_factura/$', 'grabar_factura',
        name='grabar_factura'),
    url(r'^movil/clientes/$', 'clientes',
        name='movil_clientes'),
    url(r'^movil/grud_cliente/$', 'grud_cliente',
        name='grud_cliente'),
    url(r'^movil/login/$', 'movil_login',
        name='movil_login'),
    url(r'^movil/facturas/$', 'movil_facturas',
        name='movil_facturas'),
    url(r'^tipos_pago/$', 'tipos_pago',
        name='tipos_pago'),
)
