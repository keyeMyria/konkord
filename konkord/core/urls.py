# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from . import views

# urlpatterns = [
#     url(r'^set-lang/', views.set_language),
# ]
urlpatterns = settings.APPS_URLS
