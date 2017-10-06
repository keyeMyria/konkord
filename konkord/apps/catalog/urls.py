# -*- coding: utf-8 -*-
from django.conf.urls import url
from catalog import views


urlpatterns = [
    url(r'^(?:(?P<query>(?:\w+)|(?:\w+:\S+)(?:-\w+:\S+)*))?/$', views.MainPage.as_view(), name="main_page"),
    url(
        r'^(?P<category_slug>[-\w]*)/(?P<slug>[-\w]*).html$',
        views.ProductView.as_view(),
        name="product_detail"
    ),
]
