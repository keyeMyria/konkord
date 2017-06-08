# coding: utf-8
from django import template
from django.core.urlresolvers import reverse, resolve
from django.utils import translation

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, language):
    view = resolve(context['request'].path)
    request_language = translation.get_language()
    translation.activate(language)
    url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
    translation.activate(request_language)
    return url

@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def get_dict_value(_dict, _key):
    return _dict.get(_key, None)
