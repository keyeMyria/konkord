from modeltranslation.translator import translator, TranslationOptions
from .models import SearchText


class SearchTextTranslationOptions(TranslationOptions):
    fields = (
        'search_text',
    )


translator.register(SearchText, SearchTextTranslationOptions)
