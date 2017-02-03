# -*- coding: utf-8 -*-
from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^search$', views.SearchView.as_view(), name="search"),
]
