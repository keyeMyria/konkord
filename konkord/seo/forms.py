# -*- coding: utf-8 -*-
from django import forms
from suit_ckeditor.widgets import CKEditorWidget
from codemirror.widgets import CodeMirrorTextarea
from seo.models import SEOForPage


class SeoFormMixin(object):
    class Meta:
        widgets = {
            'meta_h1_ru': CodeMirrorTextarea,
            'meta_h1_uk': CodeMirrorTextarea,
            'meta_title_ru': CodeMirrorTextarea,
            'meta_title_uk': CodeMirrorTextarea,
            'meta_keywords_ru': CodeMirrorTextarea,
            'meta_keywords_uk': CodeMirrorTextarea,
            'meta_description_ru': CodeMirrorTextarea,
            'meta_description_uk': CodeMirrorTextarea,
            'meta_seo_text_ru': CKEditorWidget,
            'meta_seo_text_uk': CKEditorWidget,
        }


class SEOForPageForm(forms.ModelForm):
    class Meta:
        model = SEOForPage
        fields = '__all__'
        widgets = {
            'meta_h1': CodeMirrorTextarea,
            'meta_title': CodeMirrorTextarea,
            'meta_keywords': CodeMirrorTextarea,
            'meta_description': CodeMirrorTextarea,
            'meta_seo_text': CKEditorWidget,
        }
