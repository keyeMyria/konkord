# -*- coding: utf-8 -*-
from adminconfig.utils import BaseConfig
from django import forms
from django.utils.translation import ugettext_lazy as _
from seo.mixins import SeoConfigMixin


class StaticPagesConfigForm(SeoConfigMixin, forms.Form):
    seo_config_prefixes = ['static_pages']


class StaticPagesConfig(SeoConfigMixin, BaseConfig):
    form_class = StaticPagesConfigForm
    block_name = 'static_pages'
    name = _('Static pages')
    seo_config_prefixes = ['static_pages']
