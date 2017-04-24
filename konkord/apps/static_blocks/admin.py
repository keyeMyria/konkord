from django.contrib import admin
from .models import StaticBlock
from modeltranslation.admin import TabbedTranslationAdmin
from .forms import StaticBlockForm


@admin.register(StaticBlock)
class StaticBlockAdmin(TabbedTranslationAdmin):
    form = StaticBlockForm
    list_display = ('identifier', 'description')
    fieldsets = [
        (None, {
            'fields': ['identifier', 'description']
        }),
        (None, {
            'fields': ['content_ru', 'content_uk']
        })
    ]
