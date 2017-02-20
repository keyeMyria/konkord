# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^subscribe$',
        views.SubscribeView.as_view(),
        name="newsletter_subscribe"),
]
