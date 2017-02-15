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


@admin.register(PageCategory)
class PageCategoryAdmin(MPTTModelAdmin):
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
                'name',
                'parent',
                'slug',
                'icon',
                'description',
                'template_category',
                'template_news',
                'pagination',
                'sort',
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': ['meta_title', 'meta_keywords', 'meta_description']
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
class PageAdmin(SortableModelAdmin):
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
                'title',
                'category',
                'slug',
                'icon',
                'template',
                'create_date',
                'active_date_start',
                'active_date_stop',
                'type',
                'show_on_full_site',
                'show_on_mobile_site',
                'vip',
                'preamble',
                'text'
            ]
        }),

        (None, {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': ['meta_title', 'meta_keywords', 'meta_description']
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
            return super(PageAdmin, self).get_fieldsets(request, obj, **kwargs)
        else:
            return self.standard_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
            })
            self.suit_form_tabs = None
            self.suit_form_includes = None
        else:
            defaults.update({
                'form': self.edit_form,
            })
            self.suit_form_tabs = self.standard_suit_form_tabs
        defaults.update(kwargs)
        return super(PageAdmin, self).get_form(request, obj, **defaults)

