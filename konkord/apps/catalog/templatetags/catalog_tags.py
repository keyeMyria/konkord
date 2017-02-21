# -*- coding: utf-8 -*-
from django.template import Library
from ..models import PropertyValueIcon
register = Library()


@register.assignment_tag
def property_value_icons_dict(product):
    p_icons = PropertyValueIcon.objects.filter(products=product)
    return {
        property.slug: icon
        for icon in p_icons
        for property in icon.properties.all()
    }
