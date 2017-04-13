from modeltranslation.translator import translator, TranslationOptions
from .models import Page, PageCategory


class PageCategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'meta_h1',
        'meta_title',
        'meta_keywords',
        'meta_description',
        'meta_seo_text'
    )


translator.register(PageCategory, PageCategoryTranslationOptions)


class PageTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'preamble',
        'text',
        'meta_h1',
        'meta_title',
        'meta_keywords',
        'meta_description',
        'meta_seo_text'
    )


translator.register(Page, PageTranslationOptions)
