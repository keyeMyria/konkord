# coding: utf-8
from django.contrib import admin
from .forms import (
    MailTemplateForm,
)

from mail.models import MailTemplate


class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')
    search_fields = ['name']
    form = MailTemplateForm
    ordering = ('name',)

admin.site.register(MailTemplate, MailTemplateAdmin)