from django.contrib import admin
from catalog.models import (
    Product, Property, ProductStatus, ProductSorting, AnalogousProducts,
    Image, ProductPropertyValue
)
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin, SortableTabularInline, SortableStackedInline
from django.utils.html import mark_safe
from .forms import ProductForm


class AnalogousProductInline(admin.TabularInline):
    model = AnalogousProducts
    extra = 0
    fk_name = 'product'
    suit_classes = 'suit-tab suit-tab-analogous'


class ProductPropertyValueInline(admin.TabularInline):
    model = ProductPropertyValue
    extra = 0
    fk_name = 'product'
    suit_classes = 'suit-tab suit-tab-property-values'


class ImageInline(SortableTabularInline):
    model = Image
    extra = 0
    suit_classes = 'suit-tab suit-tab-images'
    sortable = 'position'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'active', 'status', 'price')
    search_fields = ('name', 'uuid', 'id', 'sku', 'slug')
    list_filter = ('product_type', 'active', 'status')
    ordering = ['status__position', 'name']
    readonly_fields = ['uuid']
    actions = ['export_products_to_xls']

    prepopulated_fields = {'slug': ['name']}

    inlines = [AnalogousProductInline, ImageInline, ProductPropertyValueInline]
    form = ProductForm
    add_fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'active', 'name', 'slug', 'sku', 'status',
                'product_type', 'parent'
            ],
        }),
    ]

    edit_fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'active', 'name', 'slug', 'uuid', 'sku', 'status',
                'product_type', 'parent'
            ],
        }),
        (_(u'Description'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'short_description', 'full_description'
            ]
        }),
        (_(u'Prices'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'price', 'retail_price', 'sale', 'sale_price'
            ]
        }),
        (_(u'SEO'), {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': [
                'meta_title', 'meta_h1', 'meta_keywords', 'meta_description',
                'seo_text'
            ]
        }),
    ]
    add_suit_form_tabs = (('general', _(u'General')),)
    edit_suit_form_tabs = (
        ('general', _(u'General')),
        ('images', _(u'Images')),
        ('seo', _(u'SEO')),
        ('analogous', _(u'Analogous')),
        ('property-values', _('Property values'))
    )

    def get_fieldsets(self, request, obj):
        if obj:
            self.suit_form_tabs = self.edit_suit_form_tabs
            return self.edit_fieldsets
        else:
            self.suit_form_tabs = self.add_suit_form_tabs
            return self.add_fieldsets

    def export_products_to_xls(self, request, queryset):
        from exchange.utils import export_products_to_xls
        file = export_products_to_xls(Product.objects.all())
        self.message_user(
            request,
            mark_safe(_("File with all products available by <a href='%s'>this link</a>" % file))
        )

    export_products_to_xls.short_description = \
        _('Export products to xls')


@admin.register(ProductStatus)
class ProductStatusAdmin(SortableModelAdmin):
    list_display = (
        'name', 'show_buy_button', 'is_visible', 'in_search', 'css_class'
    )
    sortable = 'position'


@admin.register(ProductSorting)
class ProductSortingAdmin(SortableModelAdmin):
    list_display = ('name', 'order_by', 'css_class')
    sortable = 'position'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'uuid')
