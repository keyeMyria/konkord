from django.apps import AppConfig


class FiltersConfig(AppConfig):
    name = 'filters'

    def ready(self):
        from django.conf import settings
        from .settings import CHECKBOX, RADIO, SELECT, SLIDER
        settings.FILTER_PRODUCT_FUNCTION = 'filters.utils.filter_products'
        settings.FILTER_TEMPLATES = {
            CHECKBOX: 'filters/types/checkbox.html',
            RADIO: 'filters/types/radio.html',
            SELECT: 'filters/types/select.html',
            SLIDER: 'filters/types/slider.html',
        }
