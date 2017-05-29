from django.contrib import admin
from django.db import models
from django import forms
from .models import SearchText

from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(SearchText)
class SearchTextAdmin(TabbedTranslationAdmin):
    list_display = ('product', 'search_text')
    search_fields = ('product__name', 'product__slug', 'product__id')

    formfield_overrides = {
        models.CharField: {'widget': forms.widgets.Textarea},
    }
