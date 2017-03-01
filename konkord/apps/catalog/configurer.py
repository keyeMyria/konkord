# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig


class CatalogConfigForm(forms.Form):
    ignored_filters_params = forms.CharField(
        label=_('Ignored filter params'), widget=forms.TextInput,
        help_text=_(
            'Params to ignore in filters page.'
            'Each param must be defined on new line')
    )


class CatalogConfig(BaseConfig):
    form_class = CatalogConfigForm
    block_name = 'catalog'
    name = _('Catalog')
    default_data = {
        'CATALOG_IGNORED_FILTERS_PARAMS': ''
    }
    option_translation_table = (
        ('CATALOG_IGNORED_FILTERS_PARAMS', 'ignored_filters_params')
    )
