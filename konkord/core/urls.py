# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from . import views

core_urlpatterns = ([
    url(r'^set-lang/', views.set_language, name="set_language"),
], 'core')

urlpatterns = [
    url(r'^', include(core_urlpatterns)),
]

urlpatterns += settings.APPS_URLS
