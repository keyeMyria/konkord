# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.urls.resolvers import RegexURLResolver
from django.urls import resolve


class StaticPageMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            if settings.APPEND_SLASH and not request.path_info.endswith('/'):
                return HttpResponseRedirect(f'{request.path_info}/')
            is_valid_path = urlresolvers.is_valid_path(
                request.path_info, 'static_pages.urls_i18n')
            if is_valid_path:
                view, args, kwargs = resolve(
                    request.path_info, urlconf='static_pages.urls_i18n')
                kwargs['request'] = request
                return view(*args, **kwargs)
        return response
