# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from checkout.models import ShippingMethod


class DeliveryService(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=200)
    order = models.IntegerField(_('Position'), default=10)

    DS_SOURCE_CHOICES = (
        ('novaposhta', _('NovaPoshta')),
        ('delivery', _('Delivery')),
    )
    update_source = models.CharField(
        _('Update source'), default='', blank=True, max_length=30,
        choices=DS_SOURCE_CHOICES)

    class Meta:
        verbose_name = _(u'Delivery service')
        verbose_name_plural = _(u'Delivery services')
        ordering = ['order']

    def __str__(self):
        return self.name


class City(models.Model):
    title = models.CharField(
        verbose_name=_(u'Title'),
        null=True,
        blank=True,
        max_length=250
    )
    delivery_service = models.ForeignKey(
        DeliveryService,
        verbose_name=_('Delivery service'), related_name='cities')
    name = models.CharField(verbose_name=_(u'Name'), max_length=200)
    name_ua = models.CharField(
        verbose_name=_(u'Name UA'),
        max_length=200,
        blank=True)
    slug = models.SlugField(u"Slug", max_length=200)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    identificator = models.CharField(
        _('Identificator'),
        default='00000000-0000-0000-0000-000000000000',
        max_length=200)

    class Meta:
        verbose_name = _(u'City')
        verbose_name_plural = _(u'Cities')

    def __str__(self):
        return self.name


class DeliveryOffice(models.Model):
    city = models.ForeignKey(
        City, verbose_name=_(u'City'), related_name='offices')
    name = models.CharField(
        verbose_name=_(u'Name'),
        max_length=200,
        null=True,
        blank=True
    )
    address = models.TextField(verbose_name=_(u'Address'))
    phone = models.TextField(verbose_name=_(u'Phones'), null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    extra = JSONField(
        verbose_name=_(u'Extra'),
        default={}, blank=True, null=True)
    position = models.PositiveIntegerField(
        verbose_name=_(u"Position"),
        null=True,
        blank=True,
        default=0
    )
    identificator = models.CharField(
        _('Identificator'),
        default='00000000-0000-0000-0000-000000000000',
        max_length=200)

    class Meta:
        verbose_name = _(u'Delivery office')
        verbose_name_plural = _(u'Delivery offices')

    def __str__(self):
        return '%s: %s' % (self.city.name, self.address)


class DeliveryServiceRelation(models.Model):
    service = models.ForeignKey(
        DeliveryService, verbose_name=_('Delivery service'))
    shipping_method = models.OneToOneField(
        ShippingMethod,
        verbose_name=_('Shipping method'),
        related_name='delivery_service'
    )
