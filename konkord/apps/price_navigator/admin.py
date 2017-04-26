# coding: utf-8
from django.contrib import admin
from price_navigator.models import PriceNavigator
from suit.admin import SortableModelAdmin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
import price_navigator.utils
from .forms import PriceNavigatorForm


class PriceNavigatorAdmin(SortableModelAdmin, admin.ModelAdmin):
    form = PriceNavigatorForm
    sortable = 'order'
    list_display = (
        'name',
        'active',
        'file_name',
        'last_generation'
    )
    search_fields = ['name']
    actions = [
        'generate_price_navigator'
    ]

    def generate_price_navigator(self, request, queryset):

        for navigator in queryset:
            price_navigator.utils.check_tasks(navigator, True)
        self.message_user(
            request,
            _(u"The price navigator well be generated soon.")
        )
        return HttpResponseRedirect(request.path)
    generate_price_navigator.short_description = _(u"Generate")

admin.site.register(PriceNavigator, PriceNavigatorAdmin)
