from django.contrib import admin
from . import models
from . import forms
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from .utils import create_voucher_number


@admin.register(models.PaymentMethod)
class PaymentMethodAdmin(TabbedTranslationAdmin):
    pass


@admin.register(models.ShippingMethod)
class ShippingMethodAdmin(TabbedTranslationAdmin):
    pass


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

    readonly_fields = ('product',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user']
    readonly_fields = [
        'order_number', 'shipping_data', 'payment_data', 'uuid',
        'created',
        'state_modified',
        'user',
        'user_email',
        'user_phone',
        'user_data',
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
                'message',
                'price',
                'created',
                'state_modified',
                'voucher_discount'
            ],
        }),
        (_('User data'), {
            'fields': [
                'user',
                'user_email',
                'user_phone',
                'user_data'
            ],
        }),
        (_('Shipping'), {
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
    def user_phone(obj):
        return obj.get_user_phone()

    user_phone.short_description = _('User phone')

    @staticmethod
    def user_email(obj):
        return obj.get_user_email()

    user_email.short_description = _('User email')

    @staticmethod
    def shipping_city(obj):
        return obj.shipping_data.get('city', '-')

    shipping_city.short_description = _('Shipping city')

    @staticmethod
    def shipping_office(obj):
        return obj.shipping_data.get('office', '-')

    shipping_office.short_description = _('Shipping office')

    @staticmethod
    def shipping_price(obj):
        return obj.shipping_data.get('price', '-')

    shipping_price.short_description = _('Shipping price')


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
