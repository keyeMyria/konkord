# -*- coding: utf-8 -*-
from django.template import Library
from ..models import PropertyValueIcon
from django.conf import settings
register = Library()


@register.assignment_tag
def property_value_icons_dict(product):
    p_icons = PropertyValueIcon.objects.filter(products=product).values(
        'icon', 'properties__slug', 'properties__name')
    return {
        icon['properties__name']: {
            'url': settings.MEDIA_URL + icon['icon'],
            'property': icon['properties__name']
        }
        for icon in p_icons
    }
