# coding: utf-8
from django import template

register = template.Library()


@register.inclusion_tag('comparison/comparison_link.html')
def add_product_to_comparison_link(product):
    return {'product': product}
