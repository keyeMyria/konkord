from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'search'

    def ready(self):
        from django.conf import settings
        from search.urls import urlpatterns
        settings.APPS_URLS.extend(urlpatterns)
        settings.LIVE_SEARCH_LIMIT = 5
