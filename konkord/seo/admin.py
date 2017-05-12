# coding: utf-8
from django.contrib import admin

from seo.models import SEOForPage
from seo.forms import SEOForPageForm


fields_to_clear = [
    ('clear_meta_title', 'meta_title'),
    ('clear_meta_keywords', 'meta_keywords'),
    ('clear_meta_description', 'meta_description'),
]


@admin.register(SEOForPage)
class SEOForPageAdmin(admin.ModelAdmin):
    list_display = ['url', ]
    search_fields = ['url', ]
    form = SEOForPageForm
