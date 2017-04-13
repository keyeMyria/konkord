from django.apps import AppConfig


class PriceNavigatorConfig(AppConfig):
    name = 'price_navigator'

    def ready(self):
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'marketing',
            (
                'price_navigator.PriceNavigator',
            )
        )