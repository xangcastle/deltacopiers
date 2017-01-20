from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('importaciones.views',
    url(r'^calcular_flete/$', 'calcular_flete',
        name='calcular_flete'),

    url(r'^datos_proforma/$', 'datos_proforma',
        name='datos_proforma'),
)
