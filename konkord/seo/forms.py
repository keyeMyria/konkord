# -*- coding: utf-8 -*-
from suit_ckeditor.widgets import CKEditorWidget


class SeoFormMixin(object):
    class Meta:
        widgets = {
            'meta_h1_ru': CKEditorWidget,
            'meta_h1_uk': CKEditorWidget,
            'meta_title_ru': CKEditorWidget,
            'meta_title_uk': CKEditorWidget,
            'meta_keywords_ru': CKEditorWidget,
            'meta_keywords_uk': CKEditorWidget,
            'meta_description_ru': CKEditorWidget,
            'meta_description_uk': CKEditorWidget,
            'meta_seo_text_ru': CKEditorWidget,
            'meta_seo_text_uk': CKEditorWidget,
        }
