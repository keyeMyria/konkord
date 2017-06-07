from modeltranslation.translator import translator, TranslationOptions
from .models import (
    MaintenanceMessage
)


class MaintenanceMessageTranslationOptions(TranslationOptions):
    fields = (
        'message',
    )


translator.register(MaintenanceMessage, MaintenanceMessageTranslationOptions)
