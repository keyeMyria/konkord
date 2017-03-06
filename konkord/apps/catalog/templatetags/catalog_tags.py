# -*- coding: utf-8 -*-
from django.template import Library
from catalog.models import Product
from collections import OrderedDict
register = Library()


@register.simple_tag
def get_product_images(product):
    return product.images.values_list('thumbnails', flat=True)


@register.assignment_tag
def product_properties_as_dict(product):
    ppvs = product.productpropertyvalue_set.values(
        'property__slug', 'property__name', 'value')
    ppvs_dict = OrderedDict()
    for ppv in ppvs:
        ppvs_dict[ppv['property__slug']] = {
            'property_name': ppv['property__name'],
            'value': ppv['value']
        }
    return ppvs_dict
