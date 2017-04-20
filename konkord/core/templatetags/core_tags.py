# coding: utf-8
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def get_dict_value(_dict, _key):
    return _dict.get(_key, None)
