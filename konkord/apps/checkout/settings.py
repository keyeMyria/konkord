from django.utils.translation import ugettext_lazy as _
from django.conf import settings

PERCENTAGE = 'percentage'
ABSOLUTE = 'absolute'

VOUCHER_TYPE_CHOICES = (
    (PERCENTAGE, _('Percentage')),
    (ABSOLUTE, _('Absolute'))
)

MESSAGES = (
    _(u"The voucher is valid."),
    _(u"The voucher is not active."),
    _(u"The voucher has been already used."),
    _(u"The voucher is not active yet."),
    _(u"The voucher is not active any more."),
    _(u"The voucher is not valid for this cart price."),
    _(u"The voucher doesn't exist."),
)


VOUCHER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
VOUCHER_LENGTH = getattr(settings, 'VOUCHER_LENGTH', 5)
VOUCHER_PREFIX = getattr(settings, 'VOUCHER_PREFIX', "")
VOUCHER_SUFFIX = getattr(settings, 'VOUCHER_SUFFIX', "")

CART_GROUP_ITEMS_BY_PARENT = getattr(
    settings, 'CART_GROUP_ITEMS_BY_PARENT', True)
ORDER_GROUP_ITEMS_BY_PARENT = getattr(
    settings, 'ORDER_GROUP_ITEMS_BY_PARENT', CART_GROUP_ITEMS_BY_PARENT
)
