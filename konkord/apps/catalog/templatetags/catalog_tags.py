# -*- coding: utf-8 -*-
from django.template import Library
from ..models import PropertyValueIcon, Property
from django.conf import settings
from collections import OrderedDict

register = Library()


@register.assignment_tag
def property_value_icons_dict(product):
    p_icons = PropertyValueIcon.objects.filter(products=product).values(
        'icon', 'properties__slug', 'properties__name', 'description')
    return {
        icon['properties__name']: {
            'url': settings.MEDIA_URL + icon['icon'],
            'property': icon['properties__name'],
            'description': icon['description']
        }
        for icon in p_icons
    }


@register.simple_tag
def get_product_images(product):
    return product.images.values_list('thumbnails', flat=True)


@register.assignment_tag(takes_context=True)
def product_properties_as_dict(context, product):
    request = context.get('request')
    ppvs = product.productpropertyvalue_set.values(
            'property_id', 'value')
    if request and request.GET.get('pdf'):
        ppvs = ppvs.filter(property__print_to_pdf=True)
    ppvs_dict = OrderedDict()
    props = {
        prop.id: prop
        for prop in Property.objects.filter(id__in=[
            ppv['property_id'] for ppv in ppvs
        ])
    }
    for ppv in ppvs:
        prop = props[ppv['property_id']]
        ppvs_dict[prop.slug] = {
            'property_name': prop.name,
            'value': ppv['value']
        }
    return ppvs_dict
