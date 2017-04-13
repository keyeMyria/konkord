# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from seo.mixins import SeoMixin
from django.http import JsonResponse


class BreadcrumbsMixin(object):
    breadcrumbs = [(_('Main page'), '/')]
    page_type = None

    def get_breadcrumbs(self):
        return []

    def get_page_type(self):
        return self.__class__.__name__.lower().replace('view', '')

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)
        breadcrumbs = self.breadcrumbs.copy()
        additional_breadcrumbs = self.get_breadcrumbs()
        if additional_breadcrumbs:
            breadcrumbs.extend(additional_breadcrumbs)
        context.update({
            'breadcrumbs': breadcrumbs,
            'page_type': self.get_page_type()
        })
        return context


class MetaMixin(BreadcrumbsMixin, SeoMixin):
    """
    Meta mixin
    """


class JSONResponseMixin(object):
    http_method_names = ['post']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(kwargs)

    @staticmethod
    def bad_response_data(response_message=''):
        return {
            'status': 400,
            'message': 'Bad request',
            'data': {
                'message': response_message
            }
        }

    @staticmethod
    def success_response(data=None):
        if data is None:
            data = {}
        return {
            'status': 200,
            'message': 'ok',
            'data': data
        }
