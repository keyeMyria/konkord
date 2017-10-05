from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from wand.image import Image as WImage
from catalog import settings as catalog_settings
from catalog.managers import ProductManager
from django.urls import reverse
from seo.models import ModelWithSeoMixin

import uuid
import os

EMPTY = {
    'blank': True,
    'null': True
}
DECIMAL_PRICE = {
    'max_digits': 9,
    'decimal_places': 2
}


class Product(ModelWithSeoMixin, models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name=_(u'Name'), max_length=255)
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=255)
    product_type = models.IntegerField(
        verbose_name=_(u'Type of product'),
        choices=catalog_settings.PRODUCT_TYPE_CHOICES,
        default=catalog_settings.STANDARD_PRODUCT
    )
    parent = models.ForeignKey(
        'self', verbose_name=_(u'Parent'), related_name='variants', **EMPTY)
    active = models.BooleanField(verbose_name=_(u'Active'), default=False)
    status = models.ForeignKey('ProductStatus')
    sku = models.CharField(verbose_name=_(u'Sku'), max_length=100, **EMPTY)
    short_description = models.TextField(
        verbose_name=_(u'Short description'), **EMPTY)
    full_description = models.TextField(
        verbose_name=_(u'Full description'), **EMPTY)
    price = models.DecimalField(
        verbose_name=_(u'Price'), default=0.0, **DECIMAL_PRICE)
    retail_price = models.DecimalField(
        verbose_name=_(u'Retail price'), default=0.0, **DECIMAL_PRICE)
    sale = models.BooleanField(verbose_name=_(u'Sale'), default=False)
    sale_price = models.DecimalField(
        verbose_name=_(u'Sale price'), default=0.0, **DECIMAL_PRICE)

    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=9999999)

    objects = ProductManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        try:
            category = ProductPropertyValue.objects.get(
                product=self,
                property__slug="tip-obuvi"
            ).slug_value
        except ProductPropertyValue.DoesNotExist:
            category = ""

        return reverse('product_detail', kwargs={'slug': self.slug,
                                                 'category_slug': category})

    def is_variant(self):
        return self.product_type == catalog_settings.VARIANT

    def is_product_with_variants(self):
        return self.product_type == catalog_settings.PRODUCT_WITH_VARIANTS

    def is_standard(self):
        return self.product_type == catalog_settings.STANDARD_PRODUCT

    def get_price(self, *args, **kwargs):
        parent = self.parent or self
        if parent.sale:
            return parent.sale_price
        return parent.retail_price

    def get_analogous_products(self):
        return self.analogousproducts_set.order_by('order')

    @classmethod
    def fix_ordering(cls):
        from django.db.models import Min
        min_pos = Product.objects.order_by('position').aggregate(
            min_pos=Min('position'))['min_pos']
        for p in cls.objects.order_by('position'):
            if p.position < min_pos:
                p.position = min_pos
                p.save(update_fields=['position'])
                min_pos += 1
            elif p.position == min_pos:
                min_pos += 1
            else:
                min_pos = p.position + 1


class AnalogousProducts(models.Model):
    product = models.ForeignKey(Product)
    analogous_product = models.ForeignKey(
        Product,
        verbose_name=_(u'Analogous product'),
        related_name='analogous'
    )
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Analogous products')
        verbose_name_plural = _('Analogous products')


class Property(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=206)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    print_to_pdf = models.BooleanField(
        verbose_name=_('Print to pdf'), default=False)

    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    class Meta:
        ordering = ('position',)
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def __str__(self):
        return self.name


class ProductPropertyValue(models.Model):
    product = models.ForeignKey(Product)
    property = models.ForeignKey(Property, verbose_name=_(u'Value'))
    value = models.CharField(verbose_name=_(u'Value'), max_length=2096)
    slug_value = models.SlugField(verbose_name=_(u'Slug'), max_length=2096)

    class Meta:
        ordering = ('property__position',)
        verbose_name = _('Product property value')
        verbose_name_plural = _('Product property values')

    def __str__(self):
        return f'{self.product.name} {self.property.name} {self.value}'


class PropertyValueIcon(models.Model):
    properties = models.ManyToManyField(
        Property, verbose_name=_(u'Properties'))
    title = models.CharField(
        max_length=255, default='',
        blank=True, verbose_name=_(u'Icon title'))
    description = models.TextField(verbose_name=_('Description'), **EMPTY)
    position = models.SmallIntegerField(
        default=999, verbose_name=_(u'Position'))
    icon = models.ImageField(
        verbose_name=_(u'Icon'), upload_to='icons')
    products = models.ManyToManyField(
        Product, blank=True, verbose_name=_(u'Products'))
    expression = models.TextField(verbose_name=_(u'Expression for parsing'))

    class Meta:
        ordering = ('position',)
        verbose_name = _(u'Property value icon')
        verbose_name_plural = _(u'Property value icons')

    def parse(self):
        p_values = ProductPropertyValue.objects.filter(
            property__in=self.properties.all(),
            value__iregex=self.expression,
        )
        products = Product.objects.active().filter(
            productpropertyvalue__in=p_values,
            status__is_visible=True,
        )
        self.products = products
        self.save()


class ProductStatus(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=50)
    show_buy_button = models.BooleanField(
        verbose_name=_(u'Show buy button'), default=False)
    is_visible = models.BooleanField(verbose_name=_(u'Is visible'))
    in_search = models.BooleanField(verbose_name=_(u'In search'))
    css_class = models.CharField(
        verbose_name=_(u'CSS class'), max_length=100, **EMPTY)
    position = models.PositiveIntegerField(
        verbose_name=_(u'Position'), default=9999)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product status')
        verbose_name_plural = _('Product statuses')


class ProductSorting(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=255)
    order_by = models.CharField(verbose_name=_(u'Order by'), max_length=255)
    position = models.PositiveIntegerField(
        verbose_name=_(u'Position'), default=9999)
    css_class = models.CharField(
        verbose_name=_(u'CSS class'), max_length=100, **EMPTY)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product sorting')
        verbose_name_plural = _('Product sortings')


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    title = models.CharField(verbose_name=_(u'Title'), max_length=100)
    image = models.ImageField(
        _(u'Image'), upload_to='catalog/products')
    position = models.PositiveIntegerField(
        verbose_name=_(u'Position'), default=9999)

    thumbnails = JSONField(verbose_name=_(u'Thumbnails'), **EMPTY)

    class Meta:
        ordering = ['position']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def save(self, create_thumbnails=True, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        from wand.color import Color
        if create_thumbnails:
            thumbnails = {}
            original_image = WImage(filename=self.image.path)
            splitted_path = self.image.path.rsplit('.', 1)
            image_url_part = self.image.url.rsplit('/', 1)
            white_color = Color('white')
            watermark = settings.WATERMARK
            if watermark:
                watermark_img = WImage(filename=watermark.get('path'))
                image_width, image_height = original_image.size
                wm_width, wm_height = watermark_img.size
                wm_left_pos, wm_top_pos = self.watermark_position(
                    settings.WATERMARK_POSITION,
                    image_width, image_height, wm_width, wm_height)
                watermarked_original_image = original_image.clone()
                watermarked_original_image.watermark(
                    watermark_img,
                    settings.WATERMARK_TRANSPARENCY,
                    wm_left_pos,
                    wm_top_pos
                )
                original_image = watermarked_original_image
            for name, size in settings.KONKORD_IMAGE_SIZES.items():
                thumb = original_image.clone()
                thumb.transform(resize='%sx%s' % size)
                thumb.gravity = 'center'
                background = WImage().blank(background=white_color, *size)
                background.composite(
                    thumb,
                    int((background.width - thumb.width) / 2),
                    int((background.height - thumb.height) / 2),
                )
                resized_path = splitted_path.copy()
                resized_path.insert(1, 'x'.join(map(str, size)))
                joined_path = '.'.join(resized_path)
                background.save(filename=joined_path)
                image_url_part[1] = joined_path.rsplit('/', 1)[-1]
                thumbnails[name] = '/'.join(image_url_part)
            self.thumbnails = thumbnails
            self.save(create_thumbnails=False)

    def delete(self, *args, **kwargs):
        splitted_path = self.image.path.rsplit('.', 1)
        for name, size in settings.KONKORD_IMAGE_SIZES.items():
            resized_path = splitted_path.copy()
            resized_path.insert(1, 'x'.join(map(str, size)))
            try:
                os.remove('.'.join(resized_path))
            except:
                pass
        super(Image, self).delete(*args, **kwargs)

    @staticmethod
    def watermark_position(position, image_w, image_h, wm_w, wm_h):
        ''' Calculation watermark position in image.
            Return (x, y) - coordinate, where watermark must be placed (left top corner).
            Args:
                * position - place of watermark choiced in admin
                * image_w  - image width
                * image_h  - image height
                * wm_w     - watermark width
                * wm_h     - watermark height
                * delta_x_coefficient - coefficient of scaling delta x
        '''
        if isinstance(position, str):
            position = int(position)
        if position == 1:
            # place: top left
            x, y = 0, 0

        elif position == 2:
            # place: top right
            x = image_w - wm_w
            y = 0

        elif position == 3:
            # place: bottom left
            x = 0
            y = image_h - wm_h

        elif position == 4:
            # place: bottom right
            x = image_w - wm_w
            y = image_h - wm_h

        elif position == 5:
            # place: center
            x = image_w / 2 - wm_w / 2
            y = image_h / 2 - wm_h / 2

        elif position == 6:
            # place: top center
            x = image_w / 2 - wm_w / 2
            y = 0

        elif position == 7:
            # place: bottom center
            x = image_w / 2 - wm_w / 2
            y = image_h - wm_h

        elif position == 8:
            # place: right center
            x = image_w - wm_w
            y = image_h / 2 - wm_h / 2

        elif position == 9:
            # place: left center
            x = 0
            y = image_h / 2 - wm_h / 2

        return int(x), int(y)
