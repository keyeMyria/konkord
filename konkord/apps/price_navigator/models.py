# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from catalog.models import ProductStatus
from django.contrib.postgres.fields import JSONField


class PriceNavigator(models.Model):
    CODINGS = (
        (0, _('utf-8')),
        (5, _('windows-1251')),
    )

    active = models.BooleanField(_('Active'), default=False)
    name = models.CharField(_('Name'), max_length=100)
    file_name = models.CharField(_('File name'), max_length=100)
    update_times = models.CharField(
        _('Update rate'),
        max_length=300,
        help_text=_('08:00, 20:00'),
    )
    coding = models.IntegerField(_('Coding'), default=0, choices=CODINGS)
    product_statuses = models.ManyToManyField(
        ProductStatus,
        verbose_name=_('Statuses')
    )
    pack_to_zip = models.BooleanField(_('Pack to zip'), default=False)
    template = models.TextField(_('Template'))
    replacement = JSONField(
        verbose_name=_('Symbol replacement'),
        blank=True,
        null=True,
        default=''
    )
    order = models.IntegerField(default=10)
    last_generation = models.DateTimeField(
        _("Last generation"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Price navigator')
        verbose_name_plural = _('Price navigators')

    def __str__(self):
        return self.name
