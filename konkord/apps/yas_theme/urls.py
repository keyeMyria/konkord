# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = i18n_patterns(
    url(r'^browserconfig\.xml$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/apple-touch-icons/browserconfig.xml')),
    url(
        r'^sitemap/(?P<path>.*)\.xml$',
        RedirectView.as_view(
            url='/sitemap.xml')
    ),
    url(
        r'^p-reviews/(?P<path>.*)$',
        RedirectView.as_view(url='/%(path)s')
    ),
    url(
        r'^(sabo|skidka|rabochaya-obuv|zaschitnaya-obuv)$',
        RedirectView.as_view(url='/', query_string=True, permanent=True)),
    url(
        r'^c/(sabo|skidka|rabochaya-obuv|zaschitnaya-obuv)$',
        RedirectView.as_view(url='/', query_string=True, permanent=True)),
    prefix_default_language=False
)
