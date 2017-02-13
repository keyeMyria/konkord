from django.conf import settings
from .delivery import update_delivery
from .nova_poshta import update_nova_poshta


def update_cities():
    if settings.DELIVERY_UPDATE_DELIVERY_CITIES:
        update_delivery()
    if settings.DELIVERY_UPDATE_NOVA_POSHTA_CITIES:
        update_nova_poshta()
