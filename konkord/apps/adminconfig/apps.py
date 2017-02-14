from django.apps import AppConfig


class AdminConfigConfig(AppConfig):
    name = 'adminconfig'

    def ready(self):
        from django.conf import settings
        from .urls import urlpatterns
        settings.APPS_URLS.extend(urlpatterns)
