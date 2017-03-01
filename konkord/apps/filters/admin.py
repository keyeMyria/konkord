from django.contrib import admin
from .models import Filter, FilterOption
from suit.admin import SortableModelAdmin, SortableTabularInline
from django.utils.translation import ugettext_lazy as _
from .utils import generate_filters
from django.conf import settings
from modeltranslation.admin import (
    TabbedTranslationAdmin,
    TranslationTabularInline
)


class FilterOptionInline(TranslationTabularInline, SortableTabularInline):
    model = FilterOption
    extra = 0
    sortable = 'position'
    inline_actions = ['parse']


@admin.register(Filter)
class FilterAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    list_display = ['name', 'slug']
    readonly_fields = ['min_price', 'max_price']
    actions = ['parse_options', 'schedule_parse_task']

    inlines = [FilterOptionInline]
    prepopulated_fields = {'slug': ['name']}
    sortable = 'position'

    fieldsets = [
        (None, {
            'fields': [
                'name_ru', 'name_uk'
            ],
        }),
        (None, {
            'fields': [
                'help_text_ru', 'help_text_uk'
            ],
        }),
        (None, {
            'fields': [
                'type',
                'realization_type',
                'slug',
                'properties',
                'split_property_values_by',
                'popular',
                'use_option_popularity',
                'min_price',
                'max_price',
            ]
        })
    ]

    def parse_options(self, request, queryset):
        for obj in queryset:
            obj.parse()

    def schedule_parse_task(self, queryset):
        task_manager = settings.ACTIVE_TASK_QUEUE
        task_manager.schedule(generate_filters, repeat=24 * 60)

    parse_options.short_description = _('Parse options for filter')
