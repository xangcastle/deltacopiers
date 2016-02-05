# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('moneycash.produccion.views',
    url(r'^$', 'ProduccionPageView', name='producion_home'),
)