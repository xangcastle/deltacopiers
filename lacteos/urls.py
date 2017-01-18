from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('lacteos.views',
    url(r'^print/recibos/(?P<id_recoleccion>.*)/$', 'imprimir_recoleccion',name='imprimir_recoleccion'),
    url(r'^print/retenciones/(?P<id_recoleccion>.*)/$','imprimir_retencion',name='imprimir_retencion'),
    url(r'^print/productores/(?P<id_linea>.*)/$','lista_productores',name='lista_productores'),
    url(r'^print/detalle_linea/(?P<id_recoleccion>.*)/$','detalle_linea',name='detalle_linea'),
    url(r'^print/resumen_recoleccion/(?P<id_periodo>.*)/$','resumen_recoleccion',name='resumen_recoleccion'),
    url(r'^print/resumen_pago/(?P<id_periodo>.*)/$','resumen_pago',name='resumen_pago'),
)
