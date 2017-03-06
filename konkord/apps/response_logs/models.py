# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ResponseLog(models.Model):

    referer = models.TextField(
        verbose_name=_('HTTP referer'),
        blank=True)

    url = models.TextField(
        verbose_name=_('Url'),
    )
    count = models.IntegerField(
        verbose_name=_('Count'),
        default=0,
    )
    creation_date = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        verbose_name=_('Last update date'),
        auto_now=True
    )
    status_code = models.IntegerField(
        verbose_name=_(u'Status code'),
    )

    class Meta:
        verbose_name = _('Response log')
        verbose_name_plural = _('Response logs')
