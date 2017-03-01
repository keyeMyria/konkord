# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig


class SearchConfigForm(forms.Form):
    input_placeholder_ru = forms.CharField(
        label=_('Search input placeholder for ru version')
    )
    input_placeholder_uk = forms.CharField(
        label=_('Search input placeholder for uk version')
    )


class SearchConfig(BaseConfig):
    form_class = SearchConfigForm
    block_name = 'search'
    name = _('Search config')
    default_data = {
        'SEARCH_INPUT_PLACEHOLDER_RU': '',
        'SEARCH_INPUT_PLACEHOLDER_UK': '',
    }
    option_translation_table = (
        ('SEARCH_INPUT_PLACEHOLDER_RU', 'input_placeholder_ru'),
        ('SEARCH_INPUT_PLACEHOLDER_UK', 'input_placeholder_uk')
    )
