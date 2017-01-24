from django.utils.translation import ugettext_lazy as _


XLS_PRODUCT_FIELDS = [
    ('id', _('ID')),
    ('product_type', _('Product type')),
    ('parent_id', _('Parent id')),
    ('name', _('Name')),
    ('status__name', _('Status')),
    ('short_description', _('Short description')),
    ('full_description', _('Full description')),
    ('price', _('Price')),
    ('retail_price', _(u'Retail price')),
    ('property', _('Property'))
]