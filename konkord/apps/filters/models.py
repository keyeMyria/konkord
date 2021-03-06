from django.db import models
from django.utils.translation import ugettext_lazy as _
from catalog.models import (
    Product, Property, ProductPropertyValue, ProductStatus
)
from pytils.translit import slugify
import uuid
from filters.settings import (
    TYPE_CHOICES, REALIZATION_TYPE_CHOICES, PRICE,
    PROPERTY, PRODUCTS_TYPES_FOR_FILTERS, STATUS
)
from django.db.models import Min, Max
from decimal import Decimal
from filters.managers import FilterOptionManager


EMPTY = {
    'null': True,
    'blank': True
}
DECIMAL_PRICE = {
    'max_digits': 9,
    'decimal_places': 2
}


class Filter(models.Model):

    type = models.CharField(
        verbose_name=_('Type'),
        choices=TYPE_CHOICES,
        max_length=50
    )
    realization_type = models.CharField(
        verbose_name=_('Realization type'),
        choices=REALIZATION_TYPE_CHOICES,
        max_length=50
    )
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    help_text = models.CharField(
        verbose_name=_('Help text'), max_length=255, **EMPTY)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, db_index=True)
    properties = models.ManyToManyField(
        Property,
        verbose_name=_('Properties'),
        related_name='filters', blank=True)
    popular = models.BooleanField(verbose_name=_('Popular'), default=False)
    use_option_popularity = models.BooleanField(
        verbose_name=_('Use options popularity'),
        default=False
    )

    uuid = models.UUIDField(
        verbose_name=_('UUID'),
        default=uuid.uuid4, editable=False, db_index=True)
    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    min_price = models.DecimalField(
        verbose_name=_('Min price'), default=Decimal(0.0), **DECIMAL_PRICE)
    max_price = models.DecimalField(
        verbose_name=_('Max price'), default=Decimal(0.0), **DECIMAL_PRICE)
    apply_by_clicking = models.BooleanField(
        verbose_name=_('Apply by clicking'),
        default=True,
    )

    class Meta:
        ordering = ('position', )
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')

    def __str__(self):
        return self.name

    def parse(self, update_only=False, delete_old=False):

        if self.realization_type == PRICE:
            price_range = Product.objects.all().aggregate(
                min_price=Min('price'), max_price=Max('price')
            )
            self.min_price, self.max_price = (
                price_range['min_price'], price_range['max_price'])
            self.save()
            return

        if delete_old:
            self.filter_options.all().delete()
        if not update_only or delete_old or not self.filter_options.exists():
            fos_to_create = []
            if self.realization_type == PROPERTY:
                unique_ppvs = ProductPropertyValue.objects.filter(
                    property__id__in=self.properties.values_list('id', flat=True),
                    product__status__is_visible=True,
                ).order_by('value_ru').distinct('value_ru')
                max_fo_position = FilterOption.objects.filter(
                    filter=self
                ).aggregate(max_pos=Max('position'))['max_pos'] or 0
                for ppv in unique_ppvs:
                    if not FilterOption.objects.filter(
                        filter=self,
                        regex__contains=ppv.value_ru,
                    ).exists():
                        max_fo_position += 1
                        fos_to_create.append(
                            FilterOption(
                                filter=self,
                                regex=ppv.value_ru,
                                name_ru=ppv.value_ru,
                                name_uk=ppv.value_uk,
                                value=slugify(ppv.value),
                                position=max_fo_position
                            )
                        )
            elif self.realization_type == STATUS:
                statuses = ProductStatus.objects.filter(
                    is_visible=True
                ).exclude(
                    product__filter_options__id__in=
                    self.filter_options.values_list('id', flat=True)
                )
                for status in statuses:
                    fos_to_create.append(
                        FilterOption(
                            filter=self,
                            name_ru=status.name_ru,
                            name_uk=status.name_uk,
                            regex=status.name,
                            value=slugify(status.name)
                        )
                    )
            FilterOption.objects.bulk_create(fos_to_create)
        for fo in self.filter_options.all().iterator():
            fo.parse()


class FilterOption(models.Model):

    filter = models.ForeignKey(
        Filter, verbose_name=_('Filter'), related_name='filter_options')
    products = models.ManyToManyField(
        Product, verbose_name=_('Products'), related_name='filter_options',
        editable=False
    )
    products_count = models.IntegerField(
        verbose_name=_('Products count'), default=0, editable=False
    )

    name = models.CharField(verbose_name=_('Name'), max_length=255)
    regex = models.TextField(verbose_name=_('Regex'), max_length=500)
    value = models.SlugField(verbose_name=_('Value'), db_index=True, max_length=255)
    popular = models.BooleanField(verbose_name=_('Popular'), default=False)
    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    objects = FilterOptionManager()

    class Meta:
        ordering = ('position', )
        verbose_name = _('Filter option')
        verbose_name_plural = _('Filter options')

    def __str__(self):
        return self.name

    def parse(self):
        if self.filter.realization_type == PROPERTY:
            values = [val.strip() for val in self.regex.split('\n')]
            ppvs = ProductPropertyValue.objects.filter(
                property__id__in=self.filter.properties.values_list(
                    'id', flat=True),
                value__in=values
            ).values_list('id', flat=True)
            products = Product.objects.filter(
                product_type__in=PRODUCTS_TYPES_FOR_FILTERS,
                status__is_visible=True,
                productpropertyvalue__id__in=ppvs
            )
        elif self.filter.realization_type == STATUS:
            products = Product.objects.filter(
                product_type__in=PRODUCTS_TYPES_FOR_FILTERS,
                status__is_visible=True,
                status__name__icontains=self.regex
            )
        else:
            products = Product.objects.none()

        self.products = products
        self.products_count = products.count()
        self.save()
