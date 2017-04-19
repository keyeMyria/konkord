from django.conf.urls import url
from django.contrib import admin
from .admin_views import ClearCacheView

urlpatterns = [
    url(
        r'^clear-cache/$',
        admin.site.admin_view(ClearCacheView.as_view()),
        name="clear_cache"
    )
]