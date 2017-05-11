# -*- coding: utf-8 -*-
from django import template
from snippets.models import Snippet
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def snippets(context, place):
    if place == 'Head top':
        snippets = Snippet.objects.filter(place=1).order_by('position')
    elif place == 'Head bottom':
        snippets = Snippet.objects.filter(place=5).order_by('position')
    elif place == 'Body top':
        snippets = Snippet.objects.filter(place=10).order_by('position')
    elif place == 'Body bottom':
        snippets = Snippet.objects.filter(place=15).order_by('position')
    else:
        return ''

    html = ''
    for s in snippets:
        html += s.get_snippet(context)
    return mark_safe(html)
