from django.apps import AppConfig


class DeliveryConfig(AppConfig):
    name = 'delivery'

    def ready(self):
        from django.conf import settings
        settings.DELIVERY_UPDATE_DELIVERY_CITIES = False
        settings.DELIVERY_UPDATE_NOVA_POSHTA_CITIES = False
        settings.NOVA_POSHTA_API_KEY = ''
