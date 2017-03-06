# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from seo.mixins import SeoMixin


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
