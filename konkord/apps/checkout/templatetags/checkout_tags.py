# -*- coding: utf-8 -*-
from django.template import Library

register = Library()


@register.simple_tag
def get_order_items_price(items):
    price = 0
    for item in items:
        price += item.product_amount * item.product_price
    return price


@register.simple_tag
def get_cart_items_price(items):
    price = 0
    for item in items:
        price += item.amount * item.product.price
    return price
