from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = 'catalog'

    def ready(self):
        from django.conf import settings
        from catalog.urls import urlpatterns
        settings.APPS_URLS.extend(urlpatterns)
        settings.KONKORD_IMAGE_SIZES = {
            'small': (60, 60),
            'medium': (100, 100),
            'large': (400, 400),
            'huge': (600, 600)
        }
