from django.apps import AppConfig


class ExchangeConfig(AppConfig):
    name = 'exchange'

    def ready(self):
        from django.conf import settings
        from .settings import XLS_PRODUCT_FIELDS
        from catalog.settings import STANDARD_PRODUCT, VARIANT, \
            PRODUCT_WITH_VARIANTS
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'exchange',
            (
                'exchange.ImportFromXls',
            )
        )

        settings.XLS_PRODUCT_FIELDS = XLS_PRODUCT_FIELDS
        settings.XLS_PRODUCT_TYPES_MAP = {
            STANDARD_PRODUCT: getattr(
                settings, 'XLS_EXCHANGE_STANDARD_PRODUCT_ID', 'STANDARD'),
            VARIANT: getattr(settings, 'XLS_EXCHANGE_VARIANT_ID', 'VARIANT'),
            PRODUCT_WITH_VARIANTS: getattr(
                settings, 'XLS_EXCHANGE_PRODUCT_WITH_VARIANTS_ID',  'PARENT')
        }