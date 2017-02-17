from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscribe(models.Model):
    email = models.EmailField(verbose_name=_('Email'), unique=True)
    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
    
    def __str__(self):
        return self.email
