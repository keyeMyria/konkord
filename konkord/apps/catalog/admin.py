from django.contrib import admin
from catalog.models import (
    Product, Property, ProductStatus, ProductSorting, AnalogousProducts,
    Image, ProductPropertyValue, PropertyValueIcon
)
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin, SortableTabularInline
from django.utils.html import mark_safe
from .forms import ProductForm, AnalogousProductsForm, ImageForm
from modeltranslation.admin import (
    TabbedTranslationAdmin,
    TranslationTabularInline
)
from suit_sortable.admin import (
    SortableAdmin, SortableTabularInline as SuitSortableTabularInline
)
from .settings import STANDARD_PRODUCT, VARIANT, PRODUCT_WITH_VARIANTS
from django.core import urlresolvers


class ProductPropertyValueInline(TranslationTabularInline):
    model = ProductPropertyValue
    extra = 0
    fk_name = 'product'
    suit_classes = 'suit-tab suit-tab-property-values'
    prepopulated_fields = {'slug_value': ('value_ru',)}


class AnalogousProductInline(admin.TabularInline):
    model = AnalogousProducts
    form = AnalogousProductsForm
    extra = 0
    fk_name = 'product'
    suit_classes = 'suit-tab suit-tab-analogous'


class ImageInline(SortableTabularInline):
    form = ImageForm
    model = Image
    extra = 0
    suit_classes = 'suit-tab suit-tab-images'
    sortable = 'position'


class ProductInline(SuitSortableTabularInline):
    model = Product
    fields = ('name', 'position', )
    readonly_fields = ('name',)
    ordering = ['position', 'status__position', 'name']
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-variants'
    sortable = 'position'


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin, SortableAdmin):
    list_display = (
        'get_name', 'product_type', 'active', 'status', 'price')
    search_fields = ('name', 'uuid', 'id', 'sku', 'slug')
    list_filter = ('product_type', 'active', 'status')
    ordering = ['position', 'status__position', 'name']
    readonly_fields = ['uuid']
    actions = ['export_products_to_xls']

    change_form_template = 'admin/product_change_form.html'

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
        (_('Description'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'short_description_ru', 'short_description_uk',
                'full_description_ru', 'full_description_uk',
            ]
        }),
        (_('Prices'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [
                'price', 'retail_price', 'sale', 'sale_price'
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': [
                'meta_title_ru', 'meta_title_uk',
                'meta_h1_ru', 'meta_h1_uk',
                'meta_keywords_ru', 'meta_keywords_uk',
                'meta_description_ru', 'meta_description_uk',
                'meta_seo_text_ru', 'meta_seo_text_uk',
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

    def get_list_display(self, request):
        product_type_filter = request.GET.get('product_type__exact', '')
        if product_type_filter.isdigit() and int(product_type_filter) == \
                PRODUCT_WITH_VARIANTS:
            self.list_editable = ('position',)
            return self.list_display + ('position', )
        self.list_editable = []
        return self.list_display

    def get_fieldsets(self, request, obj=None, **kwargs):
        if obj:
            self.suit_form_tabs = self.edit_suit_form_tabs
            if obj.product_type == PRODUCT_WITH_VARIANTS:
                self.suit_form_tabs += ('variants', _('Variants')),
            return self.edit_fieldsets
        else:
            self.suit_form_tabs = self.add_suit_form_tabs
            return self.add_fieldsets

    def get_inline_instances(self, request, obj=None):
        inlines = self.inlines.copy()
        if obj.product_type == PRODUCT_WITH_VARIANTS:
            inlines.append(ProductInline)
        return [inline(self.model, self.admin_site) for inline in inlines]

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

    def get_name(self, obj):
        if obj.product_type == STANDARD_PRODUCT:  # Standard product
            return '<a href="%s">%s</a>' % (
                urlresolvers.reverse(
                    'admin:%s_%s_change' % (
                        'catalog', 'product'), args=[obj.pk]),
                obj.name,
            )
        elif obj.product_type == VARIANT:
            return '<img title="%s" src="/static/icons/document-small.png"'\
                '/>&nbsp;<a href="%s">%s</a>' % (
                    _('Variant'),
                    urlresolvers.reverse(
                        'admin:%s_%s_change' % (
                            'catalog', 'product'), args=[obj.pk]),
                    obj.name,
                )
        elif obj.product_type == PRODUCT_WITH_VARIANTS:
            return '''<img src="/static/icons/box-document.png" title="%s"/>
            <a href="%s">%s</a>
            <span class="pull-right">[<a href="%s">%s</a>]</span>
            ''' % (
                _(u'Product with variants'),
                urlresolvers.reverse(
                    'admin:%s_%s_change' % (
                        'catalog', 'product'), args=[obj.pk]),
                obj.name,
                '%s%s' % (
                    urlresolvers.reverse(
                        'admin:%s_%s_changelist' % (
                            'catalog', 'product')),
                    '?parent__exact=%s' % obj.pk),
                _('All variants'),
            )

    get_name.short_description = _('Name')
    get_name.allow_tags = True
    get_name.admin_order_field = 'name'


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
    list_display = ('name', 'slug', 'uuid', 'print_to_pdf')
    sortable = 'position'
    prepopulated_fields = {'slug': ['name']}
    list_editable = ('print_to_pdf', )

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
        'id', 'title', 'get_icon', 'get_product_count']
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

    def get_icon(self, obj):
        return '<img src="%s" alt="%s" />' % (
            obj.icon.url,
            obj.title.encode('utf8'),
        )
    get_icon.short_description = _(u'Icon')
    get_icon.allow_tags = True

    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = _(u'Product count')
