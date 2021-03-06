# coding: utf-8
from django.contrib import admin

from maintenance.models import MaintenanceMessage
from .forms import MaintenanceMessageForm
from modeltranslation.admin import (
    TabbedTranslationAdmin,
)


class MaintenanceMessageAdmin(TabbedTranslationAdmin):
    list_display = (
        'message', 'start_time', 'end_time', 'type')
    list_filter = ('type',)
    search_fields = ['message']
    date_hierarchy = 'start_time'
    form = MaintenanceMessageForm

admin.site.register(MaintenanceMessage, MaintenanceMessageAdmin)
