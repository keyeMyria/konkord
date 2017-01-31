from django.contrib import admin
from . import models
from . import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

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
        return f'{settings.ORDER_NUMBER_PREFIX}{obj.id}'

    order_number.short_description = _('Order number')
