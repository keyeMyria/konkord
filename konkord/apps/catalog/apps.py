from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CatalogConfig(AppConfig):
    name = 'catalog'
    verbose_name = _('Catalog')

    def ready(self):
        from django.conf import settings
        from catalog.urls import urlpatterns
        from django.conf.urls import url, include
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'catalog',
            (
                'catalog.Product',
                'catalog.Property',
                'catalog.ProductPropertyValue',
                'catalog.PropertyValueIcon',
                'catalog.ProductStatus',
                'catalog.ProductSorting',
            )
        )
        settings.APPS_URLS.extend(urlpatterns)
        settings.GROUP_PRODUCTS_BY_PARENT = True
        settings.APPS_URLS.extend([
            url(r'^autocomplete/', include('catalog.autocomplete'))
        ])
        settings.KONKORD_IMAGE_SIZES = {
            'small': (60, 60),
            'medium': (100, 100),
            'large': (200, 200),
            'huge': (600, 600),
            'mega_huge': (1000, 1000)
        }
