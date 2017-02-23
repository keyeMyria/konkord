# coding: utf-8
from django import forms
from django.contrib import admin
from price_navigator.models import PriceNavigator
from suit.admin import SortableModelAdmin
from codemirror.widgets import CodeMirrorTextarea
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
import price_navigator.utils


class PriceNavigatorForm(forms.ModelForm):

    class Meta:
        model = PriceNavigator
        widgets = {
            'template': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
        }
        exclude = []

    def clean_update_times(self):
        update_times = self.cleaned_data.get('update_times')
        if update_times:
            try:
                now = datetime.now()
                [datetime.combine(now, datetime.strptime(update_time.strip(
                    ' '), '%H:%M').time()) for update_time in update_times.split(',')]
            except:
                raise forms.ValidationError(_(u"Invalid data"))
        return update_times


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
