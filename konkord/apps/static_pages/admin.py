# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from .models import *
from .forms import (
    AddPageForm,
    EditPageForm,
    PageCategoryForm
)
from suit.admin import SortableModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(PageCategory)
class PageCategoryAdmin(TabbedTranslationAdmin, MPTTModelAdmin):
    form = PageCategoryForm
    list_display = ('name', 'slug')
    mptt_level_indent = 40
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    filter_include_ancestors = True

    standard_fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'name_ru', 'name_uk'
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'parent',
                'slug',
                'icon',
                'template_category',
                'template_news',
                'pagination',
                'sort',
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'description_ru', 'description_uk'
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': [
                'meta_h1_ru', 'meta_h1_uk',
                'meta_title_ru', 'meta_title_uk',
                'meta_keywords_ru', 'meta_keywords_uk',
                'meta_description_ru', 'meta_description_uk',
                'meta_seo_text_ru', 'meta_seo_text_uk',
            ]
        }),
    ]

    standard_suit_form_tabs = (
        ('general', _(u'General')),
        ('seo', _(u'SEO')),
    )

    class Media:
        css = {
            "all": ("/static/css/loadover.css",)
        }
        js = (
            '/static/jquery/jquery.cookie.js',
            '/static/js/sco.collapse.js',
            '/static/admin/js/ajax_links.js',
            '/static/js/loadover.js',
        )

    def get_fieldsets(self, request, obj=None, **kwargs):
        if obj is None:
            return super(PageCategoryAdmin, self).get_fieldsets(
                request, obj, **kwargs
            )
        else:
            return self.standard_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during category creation
        """
        defaults = {}
        if obj is None:
            self.suit_form_tabs = None
            self.suit_form_includes = None
        else:
            self.suit_form_tabs = self.standard_suit_form_tabs
        defaults.update(kwargs)
        return super(PageCategoryAdmin, self).get_form(request, obj, **defaults)


@admin.register(Page)
class PageAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'title',
        'template',
        'vip',
        'create_date',
        'active_date_start',
        'active_date_stop',
        'type',
    )
    list_editable = ('type',)
    sortable = 'position'
    search_fields = ['title']
    add_form = AddPageForm
    edit_form = EditPageForm
    standard_fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'title_ru', 'title_uk',
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'category',
                'slug',
                'icon',
                'template',
                'create_date',
                'active_date_start',
                'active_date_stop',
                'type',
                'vip',
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-content',),
            'fields': [
                'preamble_ru', 'preamble_uk',
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-content',),
            'fields': [
                'text_ru', 'text_uk'
            ]
        }),

        (None, {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': [
                'meta_h1_ru', 'meta_h1_uk',
                'meta_title_ru', 'meta_title_uk',
                'meta_keywords_ru', 'meta_keywords_uk',
                'meta_description_ru', 'meta_description_uk',
                'meta_seo_text_ru', 'meta_seo_text_uk'
            ]
        }),


    ]
    standard_suit_form_tabs = (
        ('general', _(u'General')),
        ('seo', _(u'SEO')),
        ('content', _(u'Content'))
    )

    class Media:
        css = {
            "all": ("/static/css/loadover.css",)
        }
        js = (
            '/static/jquery/jquery.cookie.js',
            '/static/js/sco.collapse.js',
            '/static/admin/js/ajax_links.js',
            '/static/js/loadover.js',
        )

    def get_fieldsets(self, request, obj=None, **kwargs):
        return self.standard_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
            })
        else:
            defaults.update({
                'form': self.edit_form,
            })
        self.suit_form_tabs = self.standard_suit_form_tabs
        defaults.update(kwargs)
        return super(PageAdmin, self).get_form(request, obj, **defaults)

