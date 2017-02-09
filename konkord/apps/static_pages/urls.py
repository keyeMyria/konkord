from django.conf.urls import *
from . import views


urlpatterns = [
    url(r'^(?P<category_slug>[-\w]*)/$',
        views.view_category_or_news,
        name='static_pages_category'
        ),
    url(r'^(?P<category_slug>[-\w]*)/(?P<news_slug>[-\w]*).html$',
        views.view_category_or_news,
        name='static_pages_page'
    ),
]
