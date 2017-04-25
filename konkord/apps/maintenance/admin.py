# coding: utf-8
from django.contrib import admin

from maintenance.models import MaintenanceMessage


class MaintenanceMessageAdmin(admin.ModelAdmin):
    list_display = (
        'message', 'start_time', 'end_time', 'type', 'closable')
    list_filter = ('type',)
    search_fields = ['message']
    date_hierarchy = 'start_time'

admin.site.register(MaintenanceMessage, MaintenanceMessageAdmin)
