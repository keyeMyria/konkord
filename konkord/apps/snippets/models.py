# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import Template

SNIPPET_PLACE = (
    (1, _(u'Head top')),
    (5, _(u'Head bottom')),
    (10, _(u'Body top')),
    (15, _(u'Body bottom')),
)


class Snippet(models.Model):
    name = models.CharField(_('Name'), max_length=127)
    place = models.PositiveIntegerField(_('Place'), choices=SNIPPET_PLACE)
    snippet = models.TextField(_('Snippet'))
    position = models.PositiveIntegerField(_('Position'), default=1)

    class Meta:
        verbose_name = _('Snippet')
        verbose_name_plural = _('Snippets')

    def __str__(self):
        return self.name

    def get_snippet(self, context):
        """ Render and return snippet (use default django template system)
        """
        t = Template(self.snippet)
        return t.render(context)
