from django.conf import settings
CART_GROUP_ITEMS_BY_PARENT = getattr(
    settings, 'CART_GROUP_ITEMS_BY_PARENT', True)