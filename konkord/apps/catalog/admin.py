from django.contrib import admin
from catalog.models import (
    Product, Property, ProductStatus, ProductSorting, AnalogousProducts,
    Image, ProductPropertyValue, PropertyValueIcon
)
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin, SortableTabularInline
from django.utils.html import mark_safe
from .forms import ProductForm
from modeltranslation.admin import (
    TabbedTranslationAdmin,
    TranslationTabularInline
)
from suit_sortable.admin import SortableAdmin


class ProductPropertyValueInline(TranslationTabularInline):
    model = ProductPropertyValue
    extra = 0
    fk_name = 'product'
    suit_classes = 'suit-tab suit-tab-property-values'
    prepopulated_fields = {'slug_value': ('value_ru',)}


class AnalogousProductInline(admin.TabularInline):
    model = AnalogousProducts
    extra = 0
    fk_name = 'product'
    suit_classes = 'suit-tab suit-tab-analogous'


class ImageInline(SortableTabularInline):
    model = Image
    extra = 0
    suit_classes = 'suit-tab suit-tab-images'
    sortable = 'position'


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin, SortableAdmin):
    list_display = ('name', 'product_type', 'active', 'status', 'price', 'position')
    search_fields = ('name', 'uuid', 'id', 'sku', 'slug')
    list_editable = ('position', )
    list_filter = ('product_type', 'active', 'status')
    ordering = ['position', 'status__position', 'name']
    readonly_fields = ['uuid']
    actions = ['export_products_to_xls']

    prepopulated_fields = {'slug': ['name']}

    inlines = [AnalogousProductInline, ImageInline, ProductPropertyValueInline]
    form = ProductForm

    add_fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'name_ru', 'name_uk'
            ],
        }),
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'active', 'slug', 'sku', 'status',
                'product_type', 'parent'
            ],
        }),
    ]

    edit_fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'name_ru', 'name_uk'
            ],
        }),
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'active', 'slug', 'uuid', 'sku', 'status',
                'product_type', 'parent'
            ],
        }),
        (_(u'Description'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'short_description_ru', 'short_description_uk',
                'full_description_ru', 'full_description_uk',
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
                'meta_title_ru', 'meta_title_uk',
                'meta_h1_ru', 'meta_h1_uk',
                'meta_keywords_ru', 'meta_keywords_uk',
                'meta_description_ru', 'meta_description_uk',
                'seo_text_ru', 'seo_text_uk',
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
            mark_safe(
                _("File with all products available by"
                    " <a href='%s'>this link</a>" % file)
            )
        )

    export_products_to_xls.short_description = \
        _('Export products to xls')


@admin.register(ProductStatus)
class ProductStatusAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    list_display = (
        'name', 'show_buy_button', 'is_visible', 'in_search', 'css_class'
    )
    sortable = 'position'
    fieldsets = [
        (None, {
            'fields': [
                'name_ru', 'name_uk'
            ]
        }),
        (None, {
            'fields': [
                'show_buy_button', 'is_visible', 'in_search', 'css_class'
            ]
        })
    ]


@admin.register(ProductSorting)
class ProductSortingAdmin(SortableModelAdmin):
    list_display = ('name', 'order_by', 'css_class')
    sortable = 'position'


@admin.register(Property)
class PropertyAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    list_display = ('name', 'slug', 'uuid')
    sortable = 'position'
    prepopulated_fields = {'slug': ['name']}

    fieldsets = [
        (None, {
            'fields': [
                'name_ru', 'name_uk'
            ]
        }),
        (None, {
            'fields': [
                'slug'
            ]
        })
    ]


@admin.register(PropertyValueIcon)
class PropertyValueIconAdmin(TabbedTranslationAdmin, SortableModelAdmin):
    list_display = [
        'id', 'title', 'get_icon', 'get_properties', 'get_product_count']
    search_fields = ['title']
    sortable = 'position'
    exclude = ['products']
    actions = [
        'parse_action',
    ]

    def parse_action(self, request, queryset):
        for q in queryset:
            q.parse()
    parse_action.short_description = _(u'Start parsing')

    def get_properties(self, obj):
        from django.core import urlresolvers
        properties = obj.properties.all()
        return ', '.join(['<a href="%s">%s</a>' % (
            urlresolvers.reverse(
                'admin:%s_%s_change' % ('catalog', 'property'), args=[c.pk]),
            c.name,
        ) for c in properties])
    get_properties.short_description = _(u'Properties')
    get_properties.allow_tags = True

    def get_icon(self, obj):
        return '<img src="/media/%s" alt="%s" />' % (
            obj.icon,
            obj.title.encode('utf8'),
        )
    get_icon.short_description = _(u'Icon')
    get_icon.allow_tags = True

    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = _(u'Product count')
