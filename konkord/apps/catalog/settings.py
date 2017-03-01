# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

STANDARD_PRODUCT = 0
PRODUCT_WITH_VARIANTS = 1
VARIANT = 2

PRODUCT_TYPE_LOOKUP = {
    STANDARD_PRODUCT: _(u"Standard"),
    PRODUCT_WITH_VARIANTS: _(u"Product with variants"),
    VARIANT: _(u"Variant"),
}
PRODUCT_TYPE_CHOICES = ((k, v) for k, v in PRODUCT_TYPE_LOOKUP.items())
ANALOGOUS_PRODUCTS_TYPES = getattr(
    settings, 'ANALOGOUS_PRODUCTS_TYPES', [PRODUCT_WITH_VARIANTS])