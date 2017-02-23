from django.contrib import admin
from . import models
from . import forms
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from .utils import create_voucher_number

admin.site.register(models.PaymentMethod)
admin.site.register(models.ShippingMethod)


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user']
    readonly_fields = ['order_number']
    inlines = [OrderItemInline]
    form = forms.OrderAdminForm

    @staticmethod
    def order_number(obj):
        return obj.get_number()

    order_number.short_description = _('Order number')


@admin.register(models.OrderStatus)
class OrderStatusAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    list_display = ['name']
    sortable = 'position'

    fieldsets = [
        (None, {
            'fields': [
                'name_ru', 'name_uk'
            ]
        }),
        (None, {
            'fields': [
                'slug', 'css_class', 'hex_color'
            ]
        })
    ]


@admin.register(models.Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['number', 'creator', 'creation_date', 'active']
    search_fields = ['number']
    date_hierarchy = 'creation_date'
    list_filter = ['active']
    ordering = ['-active', 'creation_date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'creator':
            kwargs['initial'] = request.user.id
        return super(VoucherAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial_data = super(
            VoucherAdmin, self).get_changeform_initial_data(request)
        initial_data['number'] = create_voucher_number()
        return initial_data
