# -*- coding: utf-8 -*-
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from . import views

urlpatterns = i18n_patterns(
    url(
        r'^(?P<slug>[-\w]*)/$',
        views.CategoryView.as_view(),
        name='static_pages_category'
    ),
)
