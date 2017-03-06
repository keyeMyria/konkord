# -*- coding: utf-8 -*-
from django.db import models
from core.utils import render_meta_info
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.translation import get_language


EMPTY = {
    'blank': True,
    'null': True,
    'default': ''
}


class ModelWithSeoMixin(models.Model):
    meta_title = models.TextField(verbose_name=_(u'Meta title'), **EMPTY)
    meta_h1 = models.TextField(verbose_name=_(u'Meta H1'), **EMPTY)
    meta_keywords = models.TextField(verbose_name=_(u'Meta keywords'), **EMPTY)
    meta_description = models.TextField(
        verbose_name=_(u'Meta description'), **EMPTY)
    meta_seo_text = models.TextField(verbose_name=_(u'SEO text'), **EMPTY)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ModelWithSeoMixin, self).__init__(*args, **kwargs)
        self._lang = get_language().upper()

    def get_context_data(self, request):
        context = {
            'request': request,
            'obj': self
        }
        return context

    def get_h1(self, request):
        if self.parent:
            return self.parent.get_h1(request)
        else:
            context = self.get_context_data(request)
            text = self.meta_h1
            if not text:
                text = getattr(
                    settings,
                    f'{self.__class__.__name__.upper()}_META_H1_{self._lang}',
                    ''
                )
            return render_meta_info(text, context)

    def get_meta_title(self, request):
        if self.parent:
            return self.parent.get_meta_title(request)
        else:
            context = self.get_context_data(request)
            text = self.meta_title
            if not text:
                text = getattr(
                    settings,
                    f'{self.__class__.__name__.upper()}_META_TITLE_{self._lang}',
                    ''
                )
            return render_meta_info(text, context)

    def get_meta_keywords(self, request):
        if self.parent:
            return self.parent.get_meta_keywords(request)
        else:
            context = self.get_context_data(request)
            text = self.meta_keywords
            if not text:
                text = getattr(
                    settings,
                    f'{self.__class__.__name__.upper()}_META_KEYWORDS_{self._lang}',
                    ''
                )
            return render_meta_info(text, context)

    def get_meta_description(self, request):
        if self.parent:
            return self.parent.get_meta_description(request)
        else:
            context = self.get_context_data(request)
            text = self.meta_description
            if not text:
                text = getattr(
                    settings,
                    f'{self.__class__.__name__.upper()}_META_DESCRIPTION_{self._lang}',
                    ''
                )
            return render_meta_info(text, context)

    def get_meta_seo_text(self, request):
        if self.parent:
            return self.parent.get_meta_seo_text(request)
        else:
            context = self.get_context_data(request)
            text = self.meta_seo_text
            if not text:
                text = getattr(
                    settings,
                    f'{self.__class__.__name__.upper()}_META_SEO_TEXT_{self._lang}',
                    ''
                )
            return render_meta_info(text, context)
