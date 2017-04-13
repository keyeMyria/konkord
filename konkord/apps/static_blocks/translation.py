from modeltranslation.translator import translator, TranslationOptions
from .models import StaticBlock


class StaticBlockTranslationOptions(TranslationOptions):
    fields = (
        'content',
    )


translator.register(StaticBlock, StaticBlockTranslationOptions)

