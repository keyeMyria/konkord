# -*- coding: utf-8 -*-
from adminconfig.utils import BaseConfig
from django import forms
from django.utils.translation import ugettext_lazy as _
from seo.mixins import SeoConfigMixin


class CatalogConfigForm(SeoConfigMixin, forms.Form):
    seo_config_prefixes = ['product', 'mainpage']
    pagination_products_on_page = forms.IntegerField(
        label=_('Products count on pagination page'),
    )

    ignored_filters_params = forms.CharField(
        label=_('Ignored filter params'), widget=forms.TextInput,
        help_text=_(
            'Params to ignore in filters page.'
            'Each param must be defined on new line'),
        required=False
    )


class CatalogConfig(SeoConfigMixin, BaseConfig):
    form_class = CatalogConfigForm
    block_name = 'catalog'
    seo_config_prefixes = ['product', 'mainpage']
    default_data = {
        'CATALOG_IGNORED_FILTERS_PARAMS': '',
        'CATALOG_PAGINATION_PRODUCTS_ON_PAGE': 10
    }
    name = _('Catalog')
    option_translation_table = (
        ('CATALOG_IGNORED_FILTERS_PARAMS', 'ignored_filters_params'),
        (
            'CATALOG_PAGINATION_PRODUCTS_ON_PAGE',
            'pagination_products_on_page'
        )
    )
