from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('tienda.views',
    url(r'^$', TiendaPageView.as_view(), name='tienda'),
)
