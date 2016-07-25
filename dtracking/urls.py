

from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('dtracking.views',
    url(r'^movil/tipos_gestion/$', 'tipos_gestion',
        name='tipos_gestion'),
    url(r'^movil/gestiones/$', 'gestiones_pendientes',
        name='gestiones_pendientes'),
    url(r'^movil/login/$', 'movil_login',
        name='dtracking_login'),
    url(r'^movil/cargar_gestion/$', 'cargar_gestion',
        name='cargar_gestion'),
    url(r'^movil/cargar_media/$', 'cargar_media',
        name='cargar_media'),
)
