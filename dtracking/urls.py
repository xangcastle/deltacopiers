

from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('dtracking.views',
    url(r'^movil/tipos_gestion/$', 'tipos_gestion',
        name='tipos_gestion'),
    url(r'^movil/gestiones/$', 'gestiones_pendientes',
        name='gestiones_pendientes'),
)
