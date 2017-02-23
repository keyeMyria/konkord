# -*- coding: utf-8 -*-
from django.template import Library
register = Library()


@register.inclusion_tag('checkout/voucher/voucher.html', takes_context=True)
def voucher(context):
    return context
