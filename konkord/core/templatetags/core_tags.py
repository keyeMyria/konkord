# coding: utf-8
from django import template
from django.core.urlresolvers import reverse, resolve
from django.utils import translation
from django.core import urlresolvers

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, language):
    request = context.get('request')
    is_valid_path = urlresolvers.is_valid_path(request.path_info)
    request_language = translation.get_language()
    if is_valid_path:
        view = resolve(
            request.path_info)
        translation.activate(language)
        url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        translation.activate(request_language)
    else:
        is_valid_path = urlresolvers.is_valid_path(
            request.path_info, 'static_pages.urls_i18n')
        if is_valid_path:
            view = resolve(
                request.path_info, urlconf='static_pages.urls_i18n')
        translation.activate(language)
        url = reverse(
            view.url_name,
            args=view.args,
            kwargs=view.kwargs,
            urlconf='static_pages.urls_i18n')
        translation.activate(request_language)
    return url


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def get_dict_value(_dict, _key):
    return _dict.get(_key, None)
