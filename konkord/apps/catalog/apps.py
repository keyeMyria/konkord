from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CatalogConfig(AppConfig):
    name = 'catalog'
    verbose_name = _('Catalog')

    def ready(self):
        from django.conf import settings
        from catalog.urls import urlpatterns
        settings.APPS_URLS.extend(urlpatterns)
        settings.GROUP_PRODUCTS_BY_PARENT = True
        settings.KONKORD_IMAGE_SIZES = {
            'small': (60, 60),
            'medium': (100, 100),
            'large': (200, 200),
            'huge': (600, 600),
            'mega_huge': (1000, 1000)
        }
