from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from wand.image import Image as WImage
from catalog import settings as catalog_settings
from catalog.managers import ProductManager
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


class Product(models.Model):
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

    # SEO
    meta_title = models.TextField(verbose_name=_(u'Meta title'), **EMPTY)
    meta_h1 = models.TextField(verbose_name=_(u'Meta H1'), **EMPTY)
    meta_keywords = models.TextField(verbose_name=_(u'Meta keywords'), **EMPTY)
    meta_description = models.TextField(
        verbose_name=_(u'Meta description'), **EMPTY)
    seo_text = models.TextField(verbose_name=_(u'SEO text'), **EMPTY)
    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=9999999)

    objects = ProductManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class AnalogousProducts(models.Model):
    product = models.ForeignKey(Product)
    analogous_product = models.ForeignKey(
        Product,
        verbose_name=_(u'Analogous product'),
        related_name='analogous'
    )

    class Meta:
        verbose_name = _('Analogous products')
        verbose_name_plural = _('Analogous products')


class Property(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=255)
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')


class ProductPropertyValue(models.Model):
    product = models.ForeignKey(Product)
    property = models.ForeignKey(Property, verbose_name=_(u'Value'))
    value = models.CharField(verbose_name=_(u'Value'), max_length=255)
    slug_value = models.SlugField(verbose_name=_(u'Slug'), max_length=255)

    class Meta:
        ordering = ('property__position',)
        verbose_name = _('Product property value')
        verbose_name_plural = _('Product property values')

    def __str__(self):
        return f'{self.product.name} {self.property.name} {self.value}'


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


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    title = models.CharField(verbose_name=_(u'Title'), max_length=100)
    image = models.ImageField(
        _(u'Image'), upload_to='catalog/products')
    position = models.PositiveIntegerField(
        verbose_name=_(u'Position'), default=9999)

    thumbnails = JSONField(verbose_name=_(u'Thumbnails'), **EMPTY)

    def save(self, create_thumbnails=True, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        if create_thumbnails:
            thumbnails = {}
            original_image = WImage(filename=self.image.path)
            splitted_path = self.image.path.rsplit('.', 1)
            image_url_part = self.image.url.rsplit('/', 1)
            for name, size in settings.KONKORD_IMAGE_SIZES.items():
                thumb = original_image.clone()
                thumb.resize(*size)
                resized_path = splitted_path.copy()
                resized_path.insert(1, 'x'.join(map(str, size)))
                joined_path = '.'.join(resized_path)
                thumb.save(filename=joined_path)
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

    class Meta:
        ordering = ['position']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
