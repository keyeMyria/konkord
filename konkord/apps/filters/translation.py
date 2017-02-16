from modeltranslation.translator import translator, TranslationOptions
from .models import Filter, FilterOption


class FilterTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'help_text',
    )


translator.register(Filter, FilterTranslationOptions)


class FilterOptionTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'value'
    )


translator.register(FilterOption, FilterOptionTranslationOptions)
