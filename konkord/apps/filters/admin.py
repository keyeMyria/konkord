from django.contrib import admin
from .models import Filter, FilterOption
from suit.admin import SortableModelAdmin, SortableTabularInline
from django.utils.translation import ugettext_lazy as _
from .utils import generate_filters
from django.conf import settings


class FilterOptionInline(SortableTabularInline):
    model = FilterOption
    extra = 0
    sortable = 'position'
    inline_actions = ['parse']


@admin.register(Filter)
class FilterAdmin(SortableModelAdmin):
    list_display = ['name', 'slug']

    actions = ['parse_options', 'schedule_parse_task']

    inlines = [FilterOptionInline]
    prepopulated_fields = {'slug': ['name']}
    sortable = 'position'

    def parse_options(self, request, queryset):
        for obj in queryset:
            obj.parse()

    def schedule_parse_task(self, queryset):
        task_manager = settings.ACTIVE_TASK_QUEUE
        task_manager.schedule(generate_filters, repeat=24 * 60)

    parse_options.short_description = _('Parse options for filter')
