# -*- coding: utf-8 -*-
from adminconfig.utils import BaseConfig
from django import forms
from codemirror.widgets import CodeMirrorTextarea
from django.utils.translation import ugettext_lazy as _


class StaticPagesConfigForm(forms.Form):
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


class StaticPagesConfig(BaseConfig):
    form_class = StaticPagesConfigForm
    block_name = 'static_pages'
    name = _('Static pages')
    default_data = {
        'STATIC_PAGES_META_H1_RU': '{{obj.title}}',
        'STATIC_PAGES_META_H1_UK': '{{obj.title}}',
        'STATIC_PAGES_META_TITLE_RU': '{{obj.title}}',
        'STATIC_PAGES_META_TITLE_UK': '{{obj.title}}',
        'STATIC_PAGES_META_KEYWORDS_RU': '',
        'STATIC_PAGES_META_KEYWORDS_UK': '',
        'STATIC_PAGES_META_DESCRIPTION_RU': '',
        'STATIC_PAGES_META_DESCRIPTION_UK': '',
        'STATIC_PAGES_META_SEO_TEXT_RU': '',
        'STATIC_PAGES_META_SEO_TEXT_UK': '',
    }
    option_translation_table = (
        ('STATIC_PAGES_META_H1_RU', 'meta_h1_ru'),
        ('STATIC_PAGES_META_H1_UK', 'meta_h1_uk'),
        ('STATIC_PAGES_META_TITLE_RU', 'meta_title_ru'),
        ('STATIC_PAGES_META_TITLE_UK', 'meta_title_uk'),
        ('STATIC_PAGES_META_KEYWORDS_RU', 'meta_keywords_ru'),
        ('STATIC_PAGES_META_KEYWORDS_UK', 'meta_keywords_uk'),
        ('STATIC_PAGES_META_DESCRIPTION_RU', 'meta_description_ru'),
        ('STATIC_PAGES_META_DESCRIPTION_UK', 'meta_description_uk'),
        ('STATIC_PAGES_META_SEO_TEXT_RU', 'meta_seo_text_ru'),
        ('STATIC_PAGES_META_SEO_TEXT_UK', 'meta_seo_text_uk'),
    )
