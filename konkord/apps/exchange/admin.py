# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import ImportFromXls
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
task_manager = settings.ACTIVE_TASK_QUEUE


class AdminImportFromXls(admin.ModelAdmin):
    list_display = ('id', 'xls_file',)
    actions = [
        'do_import'
    ]

    def do_import(self, request, queryset):
        for f in queryset:
            task_manager.schedule(
                'exchange.utils.xls_do_import',
                kwargs={'import_id': f.id},
            )
        self.message_user(
            request,
            _("Products will be imported soon.")
        )
        return HttpResponseRedirect(request.path)
    do_import.short_description = _('Import')

admin.site.register(ImportFromXls, AdminImportFromXls)
