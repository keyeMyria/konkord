from catalog.settings import VARIANT, PRODUCT_WITH_VARIANTS, STANDARD_PRODUCT
from django.utils.translation import ugettext_lazy as _
PRODUCTS_TYPES_FOR_FILTERS = [
    VARIANT, STANDARD_PRODUCT
]

SLIDER = 'slider'
CHECKBOX = 'checkbox'
SELECT = 'select'
RADIO = 'radio'


TYPE_CHOICES = (
    (SLIDER, _('Slider')),
    (CHECKBOX, _('Checkbox')),
    # (SELECT, _('Select')),
    # (RADIO, _('Radio')),
)

PRICE = 'price'
PROPERTY = 'property'
STATUS = 'status'

REALIZATION_TYPE_CHOICES = (
    (PRICE, _('Price')),
    (PROPERTY, _('Property')),
    (STATUS, _('Status'))
)