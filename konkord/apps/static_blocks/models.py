from django.db import models
from django.utils.translation import ugettext_lazy as _


class StaticBlock(models.Model):
    identifier = models.CharField(
        verbose_name=_('Identifier'),
        max_length=255
    )
    content = models.TextField(verbose_name=_('Content'))
    description = models.TextField(verbose_name=_('Description'), blank=True)

    class Meta:
        verbose_name = _('Static block')
        verbose_name_plural = _('Static blocks')

    def __str__(self):
        return self.identifier
