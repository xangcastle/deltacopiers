

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from .views import *


urlpatterns = patterns('moneycash.views',
    url(r'^$', login_required(index.as_view(), login_url='/admin/login/'),  name='moneycash'),

    url(r'^factura_venta/', login_required(factura_venta.as_view(), login_url='/admin/login/'), name='factura_venta'),
    url(r'^facturas_venta/', login_required(facturas_venta.as_view(), login_url='/admin/login/'), name='facturas_venta'),

    url(r'^autocomplete_cliente/$', 'autocomplete_cliente', name='autocomplete_cliente'),
    url(r'^autocomplete_producto/$', 'autocomplete_producto', name='autocomplete_producto'),
    url(r'^detalle_producto/$', 'detalle_producto', name='detalle_producto'),

    url(r'^roc/', login_required(roc.as_view(), login_url='/admin/login/'), name='moneycash_roc'),

    url(r'^factura_compra/', login_required(factura_compra.as_view(), login_url='/admin/login/'), name='factura_compra'),

    url(r'^bodega/', login_required(bodega.as_view(), login_url='/admin/login/'), name='moneycash_bodega'),
    url(r'^facturas_no_impresas/', login_required(facturas_no_impresas.as_view(), login_url='/admin/login/'), name='facturas_no_impresas'),
    url(r'^cierre_caja/', login_required(cierre_caja.as_view(), login_url='/admin/login/'), name='cierre_caja'),
    url(r'^depositos/', login_required(depositos.as_view(), login_url='/admin/login/'),
        name='depositos'),
    url(r'^extract_cliente/$', 'extract_cliente',
        name='extract_cliente'),
    url(r'^detalle_cliente/$', 'detalle_cliente',
        name='detalle_cliente'),
    url(r'^detalle_factura/$', 'detalle_factura',
        name='detalle_factura'),
    url(r'^grabar_factura/$', 'grabar_factura',
        name='grabar_factura'),
    url(r'^grabar_recibo/$', 'grabar_recibo',
        name='grabar_recibo'),
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
    url(r'^movil/catalogo/$', 'catalogo',
        name='catalogo'),
    url(r'^movil/register_sms/$', 'register_sms',
        name='register_sms'),
    url(r'^movil/mensajes_pendientes/$', 'mensajes_pendientes',
        name='mensajes_pendientes'),
    url(r'^movil/modelos_soportados/$', 'modelos_soportados',
        name='modelos_soportados'),
    url(r'^movil/preventa/$', 'preventa',
        name='preventa'),
    url(r'^descarga_app/$', 'descarga_app',
        name='descarga_app'),
    url(r'^descarga_cendis/$', 'descarga_cendis',
        name='descarga_cendis'),
    url(r'^generar_ecuenta/$', 'generar_ecuenta',
        name='generar_ecuenta'),
    url(r'^generar_facturas_pendientes/$', 'generar_facturas_pendientes',
        name='generar_facturas_pendientes'),
    url(r'^imprimir_factura/$', 'imprimir_factura',
        name='imprimir_factura'),

    url(r'^tableFactura/$', 'tableFactura',
        name='tableFactura'),
    url(r'^anular_factura/$', 'anular_factura',
        name='anular_factura'),
        
    url(r'^xls_ventas_cliente/', xls_ventas_cliente,
        name='xls_ventas_cliente'),
    url(r'^xls_ventas_categoria/', xls_ventas_categoria,
        name='xls_ventas_categoria'),
    url(r'^xls_catalogo_productos/', xls_catalogo_productos,
        name='xls_catalogo_productos'),
)
