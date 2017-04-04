from django.apps import AppConfig


class StaticPagesConfig(AppConfig):
    name = 'static_pages'

    def ready(self):
        from django.conf import settings
        from .urls import urlpatterns
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'static-content',
            (
                'static_pages.PageCategory',
                'static_pages.Page'
            )
        )

        settings.APPS_URLS.extend(urlpatterns)
        settings.STATIC_PAGES_VIEW_CHILD_NEWS = False
        settings.MIDDLEWARE.insert(
            0, 'static_pages.middlewares.StaticPageMiddleware')
