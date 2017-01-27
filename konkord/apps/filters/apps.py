from django.apps import AppConfig


class FiltersConfig(AppConfig):
    name = 'filters'

    def ready(self):
        from django.conf import settings
        settings.FILTER_PRODUCT_FUNCTION = 'filters.utils.filter_products'
