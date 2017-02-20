# -*- coding: utf-8 -*-
from django.template import Library
from collections import deque
from itertools import count
register = Library()


@register.inclusion_tag('newsletter/subscribe.html', takes_context=True)
def newsletter_subscribe_form(context):
    return context

