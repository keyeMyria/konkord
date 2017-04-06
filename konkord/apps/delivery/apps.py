from django.apps import AppConfig


class DeliveryConfig(AppConfig):
    name = 'delivery'

    def ready(self):
        from core import add_to_suit_config_menu
        add_to_suit_config_menu(
            'delivery',
            (
                'delivery.DeliveryService',
                'delivery.City',
                'delivery.DeliveryServiceRelation'
            )
        )
