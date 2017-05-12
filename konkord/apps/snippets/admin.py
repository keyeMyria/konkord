# -*- coding: utf-8 -*-

from django.contrib import admin
from suit.admin import SortableModelAdmin

from snippets.models import Snippet


class SnippetAdmin(SortableModelAdmin):
    display_list = ['name',]
    sortable = 'position'

admin.site.register(Snippet, SnippetAdmin)
