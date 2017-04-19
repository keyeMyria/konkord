from django.contrib import admin
from .models import SearchText

from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(SearchText)
class SearchTextAdmin(TabbedTranslationAdmin):
    list_display = ('product', 'search_text')
    search_fields = ('product__name', 'product__slug', 'product__id')
