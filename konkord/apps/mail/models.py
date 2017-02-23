from django.db import models
from django.utils.translation import ugettext_lazy as _


class MailTemplate(models.Model):
    name = models.CharField(
        _('Template name'), max_length=100, default='')
    comment = models.CharField(
        _('Info'), max_length=255, default='', blank=True, null=True)
    html_template = models.TextField(_('HTML'), default='')

    class Meta:
        verbose_name = _('Mail template')
        verbose_name_plural = _('Mail templates')

    def __str__(self):
        return self.name
