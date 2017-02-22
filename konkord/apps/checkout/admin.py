from django.contrib import admin
from . import models
from . import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

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
    readonly_fields = [
        'order_number', 'shipping_data', 'payment_data', 'uuid',
        'created',
        'state_modified',
        'user_email',
        'shipping_city',
        'shipping_office',
        'shipping_price',
    ]
    inlines = [OrderItemInline]
    form = forms.OrderAdminForm

    fieldsets = (
        (None, {
            'fields': [
                'order_number',
                'status',
                'price',
                'message',
                'created',
                'state_modified'
            ],
        }),
        (_('User data'), {
            'classes': ('collapse',),
            'fields': [
                'user',
                'user_email',
            ],
        }),
        (_('Shipping'), {
            'classes': ('collapse',),
            'fields': [
                'shipping_method',
                'shipping_city',
                'shipping_office',
                'shipping_price',
            ],
        }),
        (_('Payment'), {
            'classes': ('collapse',),
            'fields': [
                'payment_method',
            ],
        }),
        (_('Extra'), {
            'classes': ('collapse',),
            'fields': ['extra_data'],
        }),
    )

    @staticmethod
    def order_number(obj):
        return obj.get_number()

    order_number.short_description = _('Order number')

    @staticmethod
    def user_email(obj):
        return obj.user.email

    @staticmethod
    def shipping_city(obj):
        return obj.shipping_data.get('city', '-')

    @staticmethod
    def shipping_office(obj):
        return obj.shipping_data.get('office', '-')

    @staticmethod
    def shipping_price(obj):
        return obj.shipping_data.get('price', '-')


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
