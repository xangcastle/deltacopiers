# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='moneycash'),
    url(r'^modules/$', ModulesPage.as_view(), name='modules'),
]
