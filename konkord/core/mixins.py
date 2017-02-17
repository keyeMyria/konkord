# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


class MetaMixin(object):
    breadcrumbs = [(_('Main page'), '/')]

    def get_breadcrumbs(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(MetaMixin, self).get_context_data(**kwargs)
        breadcrumbs = self.breadcrumbs.copy()
        additional_breadcrumbs = self.get_breadcrumbs()
        if additional_breadcrumbs:
            breadcrumbs.extend(additional_breadcrumbs)
        context['breadcrumbs'] = breadcrumbs
        return context
