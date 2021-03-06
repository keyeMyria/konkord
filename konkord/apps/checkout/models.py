from django.db import models
from django.utils.translation import ugettext_lazy as _
from catalog.models import Product
from core.fields import UnicodeJSONField
from users.models import User
import uuid
from django.conf import settings
from django.db.models import Sum, F, Case, When
from decimal import Decimal
from .settings import VOUCHER_TYPE_CHOICES, ABSOLUTE, PERCENTAGE, MESSAGES
from datetime import datetime, date
from .managers import CartManager
from catalog.settings import VARIANT
from collections import defaultdict
from .settings import CART_GROUP_ITEMS_BY_PARENT, ORDER_GROUP_ITEMS_BY_PARENT


EMPTY = {
    'null': True,
    'blank': True
}
DECIMAL_PRICE = {
    'max_digits': 9,
    'decimal_places': 2
}

EMPTY_DECIMAL_PRICE = {
    'null': True,
    'blank': True,
    'max_digits': 9,
    'decimal_places': 2
}

# TODO methods can have base model


class PaymentMethod(models.Model):
    active = models.BooleanField(_(u"Active"), default=False)
    name = models.CharField(_(u"Name"), max_length=50)
    description = models.TextField(_(u"Description"), **EMPTY)
    price = models.DecimalField(
        _(u"Price"), default=Decimal(0.0), **DECIMAL_PRICE)

    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    class Meta:
        ordering = ("position", )
        verbose_name = _(u'Payment method')
        verbose_name_plural = _(u'Payment methods')

    def __str__(self):
        return self.name

    def get_price(self, **kwargs):
        return self.price


class ShippingMethod(models.Model):
    active = models.BooleanField(_(u"Active"), default=False)
    name = models.CharField(_(u"Name"), max_length=50)
    description = models.TextField(_(u"Description"), **EMPTY)
    price = models.DecimalField(
        _(u"Price"), default=Decimal(0.0), **DECIMAL_PRICE)

    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    class Meta:
        ordering = ("position", )
        verbose_name = _(u'Shipping method')
        verbose_name_plural = _(u'Shipping methods')

    def __str__(self):
        return self.name

    def get_price(self, **kwargs):
        return self.price


class Cart(models.Model):
    GROUP_ITEMS_BY_PARENT = CART_GROUP_ITEMS_BY_PARENT

    user = models.OneToOneField(
        User, verbose_name=_(u"User"), **EMPTY)
    session = models.CharField(_(u"Session"), max_length=100, **EMPTY)
    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True
    )
    extra = UnicodeJSONField(verbose_name=_('Extra'), **EMPTY)
    language = models.CharField(
        verbose_name=_('Language'), max_length=50, null=True)

    objects = CartManager()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def get_items(self):
        if self.GROUP_ITEMS_BY_PARENT:
            items_dict = defaultdict(list)
            standard_products = []
            for item in self.items.all():
                product = item.product
                if product.product_type == VARIANT and product.parent:
                    items_dict[product.parent].append(item)
                else:
                    standard_products.append(item)
            items = []
            for parent_product, variants in items_dict.items():
                items.append((parent_product, variants))
            items.append((None, standard_products))
            return items
        else:
            return self.items.all()

    def get_total_amount(self):
        return self.items.aggregate(total_amount=Sum('amount'))['total_amount']

    def get_total_price(self):
        return self.items.annotate(
            item_price=Case(
                When(
                    product__parent__sale=True,
                    then=F('product__parent__sale_price')
                ),
                default=F('product__parent__retail_price')
            )
        ).aggregate(
            total_price=Sum(
                F('amount') * F('item_price'),
                output_field=models.DecimalField())
        )['total_price']


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart, related_name='items', verbose_name=_('Cart'))
    product = models.ForeignKey(
        Product, related_name='+', verbose_name=_('Product'))
    amount = models.IntegerField(verbose_name=_('Amount'), default=0)
    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True
    )

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')

    def __str__(self):
        return self.product.name

    def get_price(self):
        return self.product.get_price() * self.amount


class Order(models.Model):
    GROUP_ITEMS_BY_PARENT = ORDER_GROUP_ITEMS_BY_PARENT

    created = models.DateTimeField(_("Created"), auto_now_add=True)

    user = models.ForeignKey(
        User, verbose_name=_('User'), related_name='orders', **EMPTY)

    user_data = UnicodeJSONField(
        verbose_name=_('User data'),
        default=dict()
    )

    language = models.CharField(
        verbose_name=_('Language'), max_length=50, null=True)

    price = models.DecimalField(
        _("Price"), default=Decimal(0.0), **DECIMAL_PRICE)

    shipping_data = UnicodeJSONField(
        _(u'Shipping data'), default=dict(), **EMPTY)
    shipping_method = models.ForeignKey(
        ShippingMethod, verbose_name=_("Shipping Method"), **EMPTY)

    voucher = models.ForeignKey('Voucher', verbose_name=_('Voucher'), **EMPTY)
    voucher_discount = models.DecimalField(
        _("Voucher discount"), default=Decimal(0.0), **EMPTY_DECIMAL_PRICE)

    payment_data = UnicodeJSONField(
        _(u'Payment data'), default=dict(), blank=True)
    payment_method = models.ForeignKey(
        PaymentMethod, verbose_name=_("Payment Method"), **EMPTY)

    uuid = models.UUIDField(editable=False, default=uuid.uuid4)

    extra_data = UnicodeJSONField(_(u'Extra data'), default=dict(), blank=True)

    status = models.ForeignKey('OrderStatus', verbose_name=_('State'))

    state_modified = models.DateTimeField(
        _("State modified"), auto_now=True)

    message = models.TextField(
        verbose_name=_('Message'), **EMPTY)
    user_message = models.TextField(
        verbose_name=_('User message'), **EMPTY
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.get_number()} {self.uuid}'

    def get_user_full_name(self):
        full_name = self.user_data.get('full_name')
        if not full_name:
            first_name = self.get_user_first_name()
            last_name = self.get_user_last_name()
            if first_name and last_name:
                return '%s %s' % (first_name, last_name)
        return full_name

    def get_user_first_name(self):
        first_name = self.user_data.get('first_name', '')
        if not first_name and self.user:
            return self.user.first_name
        return first_name

    def get_user_last_name(self):
        last_name = self.user_data.get('last_name', '')
        if not last_name and self.user:
            return self.user.last_name
        return last_name

    def get_user_email(self):
        email = self.user_data.get('email', '')
        if not email and self.user:
            email = self.user.emails.first()
            if email:
                return email.email
        return email

    def get_user_phone(self):
        phone = self.user_data.get('phone', '')
        if not phone and self.user:
            phone = self.user.phones.first()
            if phone:
                return phone.number
        return phone

    def get_items(self):
        if self.GROUP_ITEMS_BY_PARENT:
            items_dict = defaultdict(list)
            standard_products = []
            for item in self.items.all():
                product = item.product
                if product and product.product_type == VARIANT and \
                        product.parent:
                    items_dict[product.parent].append(item)
                else:
                    standard_products.append(item)
            items = []
            for parent_product, variants in items_dict.items():
                items.append((parent_product, variants))
            items.append((None, standard_products))
            return items
        else:
            return self.items.all()

    @staticmethod
    def get_default_status():
        default = getattr(settings, 'DEFAULT_ORDER_STATUS', None)
        if default is None:
            if not OrderStatus.objects.exists():
                o, created = OrderStatus.objects.get_or_create(
                    name='', slug="submitted")
                return o
            else:
                return OrderStatus.objects.first()
        else:
            return OrderStatus.objects.get(pk=default)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status is None:
            self.status = self.get_default_status()
        return super(Order, self).save(
            force_insert, force_update, using, update_fields)

    def get_number(self):
        return f'{settings.ORDER_NUMBER_PREFIX}{self.id}'

    def payment_price(self):
        if self.payment_method:
            return self.payment_method.get_price()
        else:
            return 0

    def shipping_price(self):
        if self.shipping_method:
            return self.shipping_method.get_price()
        else:
            return 0

    def get_products_price(self):
        return self.items.annotate(
            item_price=Case(
                When(
                    product__parent__sale=True,
                    then=F('product__parent__sale_price')
                ),
                default=F('product__parent__retail_price')
            )
        ).aggregate(
            total_price=Sum(
                F('product_amount') * F('item_price'),
                output_field=models.DecimalField())
        )['total_price']
    
    def get_total_price(self):
        return self.get_products_price() + self.shipping_price() + self.payment_price()
        


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items")
    product = models.ForeignKey(
        Product,
        verbose_name=_(u'Product'),
        blank=True,
        null=True, on_delete=models.SET_NULL)

    product_amount = models.IntegerField(
        _(u"Product quantity"), blank=True, null=True)
    product_name = models.CharField(
        _(u"Product name"), blank=True, max_length=300)
    product_price = models.DecimalField(
        _(u"Product price"), default=Decimal(0.0), **DECIMAL_PRICE)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f'{self.order.get_number} {self.get_name()}'

    def get_total_price(self):
        return self.product_amount * self.product_price

    def get_name(self):
        if self.product:
            return self.product.name
        return self.product_name


class OrderStatus(models.Model):
    name = models.CharField(_(u"Name"), max_length=255)
    slug = models.SlugField(_(u'Identifier'))
    css_class = models.CharField(_(u"CSS class"), max_length=255)
    hex_color = models.CharField(
        _(u'Hex color'), max_length=7, default='#ffffff')
    position = models.PositiveIntegerField(
        verbose_name=_('Position'), default=0)

    class Meta:
        ordering = ['position']
        verbose_name = _('Order status')
        verbose_name_plural = _('Order statuses')

    def __str__(self):
        return self.name


class Voucher(models.Model):
    """A voucher.

    Parameters:

        - number
            The unique number of the voucher. This number has to be provided
            by the shop customer within the checkout in order to get the
            credit.

        - group
            The group the voucher belongs to.

        - creator
            The creator of the voucher

        - creation_date
            The date the voucher has been created

        - start_date
            The date the voucher is going be valid. Before that date the
            voucher can't be used.

        - end_date
            The date the voucher is going to expire. After that date the
            voucher can't be used.

        - effective_from
            The cart price the voucher is from that the voucher is valid.

        - kind_of
            The kind of the voucher. Absolute or percentage.

        - value
            The value of the the voucher, which is interpreted either as an
            absolute value in the current currency or a percentage quotation.

        - active
            Only active vouchers can be redeemed.

        - used
            Indicates whether a voucher has already be used. Every voucher can
            only used one time.

        - used_date
            The date the voucher has been redeemed.

        - The quanity of how often the voucher can be used. Let it empty
          the voucher can be used unlimited.
    """
    name = models.CharField(_('Name'), max_length=255, null=True)
    number = models.CharField(
        _('Voucher number'), max_length=100, unique=True)
    creator = models.ForeignKey(User, verbose_name=_('Creator'))
    creation_date = models.DateTimeField(
        _('Creation date'), auto_now_add=True)
    start_date = models.DateField(_('Start date'), blank=True, null=True)
    effective_from = models.FloatField(
        _('Effective from'), default=0.0, help_text=_('Minimal price'))
    end_date = models.DateField(
        _('End date'), blank=True, null=True)
    type = models.CharField(
        _('Discount type'), choices=VOUCHER_TYPE_CHOICES, max_length=100)
    value = models.DecimalField(
        _(u'Value'), default=Decimal(0.0), **DECIMAL_PRICE)
    active = models.BooleanField(_(u'Active'), default=True)
    used_amount = models.PositiveSmallIntegerField(
        _(u'Used amount'), default=0)
    last_used_date = models.DateTimeField(
        _(u'Last used date'), blank=True, null=True)
    limit = models.PositiveSmallIntegerField(
        _(u'Limit'), blank=True, null=True, default=1)

    class Meta:
        ordering = ("creation_date", "number")
        verbose_name = _(u'Voucher')
        verbose_name_plural = _(u'Vouchers')

    def __str__(self):
        return self.number

    def get_discount(self, cart_price):
        if self.type == ABSOLUTE:
            return self.value
        else:
            return cart_price * (self.value / Decimal(100))

    def mark_as_used(self):
        self.used_amount += 1
        self.last_used_date = datetime.now()
        if self.limit:
            if self.used_amount >= self.limit:
                self.active = False
        self.save()

    def is_effective(self, cart_price):
        if self.active is False:
            return False, str(MESSAGES[1])
        if (self.limit > 0) and (self.used_amount >= self.limit):
            return False, str(MESSAGES[2])
        if self.start_date and self.start_date > date.today():
            return False, str(MESSAGES[3])
        if self.end_date and self.end_date < date.today():
            return False, str(MESSAGES[4])
        if self.effective_from > cart_price:
            return False, str(MESSAGES[5])

        return True, str(MESSAGES[0])

    def is_absolute(self):
        return self.type == ABSOLUTE

    def is_percentage(self):
        return self.type == PERCENTAGE
