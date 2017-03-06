# -*- coding: utf-8 -*-
from adminconfig.utils import BaseConfig
from django import forms
from codemirror.widgets import CodeMirrorTextarea
from django.utils.translation import ugettext_lazy as _


class CatalogConfigForm(forms.Form):
    ignored_filters_params = forms.CharField(
        label=_('Ignored filter params'), widget=forms.TextInput,
        help_text=_(
            'Params to ignore in filters page.'
            'Each param must be defined on new line')
    )
    meta_h1_ru = forms.CharField(
        label=_('Meta H1 [ru]'), widget=CodeMirrorTextarea, required=False)
    meta_h1_uk = forms.CharField(
        label=_('Meta H1 [uk]'), widget=CodeMirrorTextarea, required=False)

    meta_title_ru = forms.CharField(
        label=_('Meta title [ru]'), widget=CodeMirrorTextarea, required=False)
    meta_title_uk = forms.CharField(
        label=_('Meta title [uk]'), widget=CodeMirrorTextarea, required=False)

    meta_keywords_ru = forms.CharField(
        label=_('Meta keywords [ru]'),
        widget=CodeMirrorTextarea,
        required=False
    )
    meta_keywords_uk = forms.CharField(
        label=_('Meta keywords [uk]'),
        widget=CodeMirrorTextarea,
        required=False
    )

    meta_description_ru = forms.CharField(
        label=_('Meta description [ru]'),
        widget=CodeMirrorTextarea,
        required=False
    )
    meta_description_uk = forms.CharField(
        label=_('Meta description [uk]'),
        widget=CodeMirrorTextarea,
        required=False
    )

    meta_seo_text_ru = forms.CharField(
        label=_('Meta seo text [ru]'),
        widget=CodeMirrorTextarea,
        required=False
    )
    meta_seo_text_uk = forms.CharField(
        label=_('Meta seo text [uk]'),
        widget=CodeMirrorTextarea,
        required=False
    )


class CatalogConfig(BaseConfig):
    form_class = CatalogConfigForm
    block_name = 'catalog'
    name = _('Catalog')
    default_data = {
        'CATALOG_IGNORED_FILTERS_PARAMS': '',
        'PRODUCT_META_H1_RU': '',
        'PRODUCT_META_H1_UK': '',
        'PRODUCT_META_TITLE_RU': '',
        'PRODUCT_META_TITLE_UK': '',
        'PRODUCT_META_KEYWORDS_RU': '',
        'PRODUCT_META_KEYWORDS_UK': '',
        'PRODUCT_META_DESCRIPTION_RU': '',
        'PRODUCT_META_DESCRIPTION_UK': '',
        'PRODUCT_META_SEO_TEXT_RU': '',
        'PRODUCT_META_SEO_TEXT_UK': '',
    }
    option_translation_table = (
        ('CATALOG_IGNORED_FILTERS_PARAMS', 'ignored_filters_params'),
        ('PRODUCT_META_H1_RU', 'meta_h1_ru'),
        ('PRODUCT_META_H1_UK', 'meta_h1_uk'),
        ('PRODUCT_META_TITLE_RU', 'meta_title_ru'),
        ('PRODUCT_META_TITLE_UK', 'meta_title_uk'),
        ('PRODUCT_META_KEYWORDS_RU', 'meta_keywords_ru'),
        ('PRODUCT_META_KEYWORDS_UK', 'meta_keywords_uk'),
        ('PRODUCT_META_DESCRIPTION_RU', 'meta_description_ru'),
        ('PRODUCT_META_DESCRIPTION_UK', 'meta_description_uk'),
        ('PRODUCT_META_SEO_TEXT_RU', 'meta_seo_text_ru'),
        ('PRODUCT_META_SEO_TEXT_UK', 'meta_seo_text_uk'),
    )
