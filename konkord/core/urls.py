# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from . import views
from django.contrib.sitemaps.views import sitemap, index
from .sitemap import ProductSitemap

core_urlpatterns = ([
    url(r'^set-lang/', views.set_language, name="set_language"),
], 'core')

urlpatterns = [
    url(r'^', include(core_urlpatterns)),
    url(
        r'^sitemap\.xml$', index,
        {
            'sitemaps': {'product': ProductSitemap},
        }
    ),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        sitemap, {'sitemaps': {'product': ProductSitemap}},
        name='django.contrib.sitemaps.views.sitemap'
    )
]

urlpatterns += settings.APPS_URLS
