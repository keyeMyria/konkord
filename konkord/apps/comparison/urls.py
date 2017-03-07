# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ComparisonView.as_view(), name="comparison"),
    url(
        r'^add$',
        views.AddProductView.as_view(),
        name="comparison_add_product"
    ),
    url(
        r'^remove$',
        views.RemoveProductsView.as_view(),
        name="comparison_remove_products"
    ),
    url(
        r'^products$',
        views.ComparisonProductsView.as_view(),
        name="comparison_products"
    ),
]
