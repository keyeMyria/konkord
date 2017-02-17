from django.conf.urls import *
from . import views


urlpatterns = [
    url(
        r'^(?P<category_slug>[-\w]*)/(?P<page_slug>[-\w]*).html$',
        views.PageView.as_view(),
        name='static_pages_page'
    ),
]
