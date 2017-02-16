from django.apps import AppConfig


class StaticPagesConfig(AppConfig):
    name = 'static_pages'

    def ready(self):
        from django.conf import settings
        from .urls import urlpatterns
        settings.APPS_URLS.extend(urlpatterns)
        settings.STATIC_PAGES_VIEW_CHILD_NEWS = False
