# -*- coding: utf-8 -*-
from django.conf.urls import url
from catalog import views


urlpatterns = [
    url(r'^$', views.MainPage.as_view(), name="main_page"),
    url(r'^(?P<slug>[-\w]*)$', views.ProductView.as_view(), name="product_detail"),
]
