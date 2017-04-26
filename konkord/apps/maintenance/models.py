# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from django.conf import settings


MESSAGE_TYPES = (
    (0, _('Announce for admins')),
    (5, _('Announce both for admins and users')),
    (10, _('Message for users')),
    (15, _('Full site down')),
)


class MaintenanceMessage(models.Model):
    message = models.TextField(_('Message'))
    start_time = models.DateTimeField(_('Start time'), default=timezone.now)
    end_time = models.DateTimeField(_('End time'), blank=True, null=True)
    type = models.IntegerField(
        _('Message type'), default=0, choices=MESSAGE_TYPES)

    class Meta:
        verbose_name = _('Maintenance message')
        verbose_name_plural = _('Maintenance messages')

    def __str__(self):
        return self.message

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        obj = super(MaintenanceMessage, self).save()
        if not getattr(settings, 'MAINTENANCE_CACHE_MESSAGES', False):
            cache.delete('maintenance_messages')
        return obj
