# coding: utf-8
from django import template

register = template.Library()


@register.inclusion_tag('comparison/comparison_icon.html')
def comparison_icon(product):
    return {'product': product}
