# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from catalog.models import ProductStatus
from django.contrib.postgres.fields import JSONField


class PriceNavigator(models.Model):
    CODINGS = (
        (0, _(u'utf-8')),
        (5, _(u'windows-1251')),
    )

    active = models.BooleanField(_(u'Active'), default=False)
    name = models.CharField(_(u'Name'), max_length=100)
    file_name = models.CharField(_(u'File name'), max_length=100)
    update_times = models.CharField(
        _(u'Update rate'),
        max_length=300,
        help_text=_(u'08:00, 20:00'),
        null=True,
    )
    coding = models.IntegerField(_(u'Coding'), default=0, choices=CODINGS)
    product_statuses = models.ManyToManyField(
        ProductStatus,
        verbose_name=_(u'Statuses')
    )
    pack_to_zip = models.BooleanField(_(u'Pack to zip'), default=False)
    template = models.TextField(_(u'Template'))
    replacement = JSONField(
        verbose_name=_(u'Symbol replacement'),
        blank=True,
        null=True,
        default=''
    )
    order = models.IntegerField(default=10)
    last_generation = models.DateTimeField(
        _(u"Last generation"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _(u'Price navigator')
        verbose_name_plural = _(u'Price navigators')

    def __str__(self):
        return self.name
