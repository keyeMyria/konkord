from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'search'

    def ready(self):
        from django.conf import settings
        from search.urls import urlpatterns
        from core import add_to_suit_config_menu
        add_to_suit_config_menu(
            'catalog',
            (
                'search.SearchText',
            )
        )
        settings.APPS_URLS.extend(urlpatterns)
        settings.LIVE_SEARCH_LIMIT = 5
