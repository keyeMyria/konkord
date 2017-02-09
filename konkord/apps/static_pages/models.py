# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel
from datetime import datetime
from .settings import TEMPLATES
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


SORT_CHOICES = (
    (1, _(u'Direct')),
    (2, _(u'Reverse')),
)


class PageCategory(MPTTModel):
    name = models.CharField(max_length=200, verbose_name=_(u"Category name"))
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name=_(u"Parent")
    )
    slug = models.SlugField(u"Slug", unique=True, max_length=200)
    icon = models.ImageField(
        verbose_name=_(u'Icon'),
        upload_to='static_pages_category_icons',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name=_(u"Description"),
        blank=True,
        null=True
    )
    template_category = models.CharField(
        choices=TEMPLATES,
        verbose_name=_(u"Rubric template"),
        max_length=200,
        default='default.html'
    )
    template_news = models.CharField(
        choices=TEMPLATES,
        verbose_name=_(u"Article template"),
        max_length=200,
        default='default.html'
    )
    pagination = models.IntegerField(
        verbose_name=_(u"Count of articles per page"), default=30)
    sort = models.IntegerField(
        choices=SORT_CHOICES,
        verbose_name=_(u'Sort')
    )

    meta_title = models.TextField(_(u"Meta Title"), blank=True)
    meta_keywords = models.TextField(_(u"Meta Keywords"), blank=True)
    meta_description = models.TextField(_(u"Meta Description"), blank=True)
    meta_seo_text = models.TextField(_(u"Meta Text"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Page category")
        verbose_name_plural = _(u"Pages categories")

    class MPTTMeta:
        order_insertion_by = ['name', ]

    def get_meta_title(self, request=None, context=None):
        data = {
            'name': self.name,
        }
        if self.meta_title != '':
            title = self.meta_title
        else:
            title = settings.SBITS_PAGES_META_TITLE
        return render_to_string(title, data)

    def get_meta_keywords(self, request=None, context=None):
        data = {
            'name': self.name,
        }
        if self.meta_keywords != '':
            meta_keywords = self.meta_keywords
        else:
            meta_keywords = settings.SBITS_PAGES_META_KEYWORDS
        return render_to_string(meta_keywords, data)

    def get_meta_description(self, request=None, context=None):
        data = {
            'name': self.name,
        }
        if self.meta_description != '':
            meta_description = self.meta_description
        else:
            meta_description = settings.SBITS_PAGES_META_DESCRIPTION
        return render_to_string(meta_description, data)

    def get_meta_seo_text(self, request=None, context=None):
        data = {
            'name': self.name,
        }
        return render_to_string(self.meta_seo_text, data)

    def get_absolute_url(self):
        return reverse(
            "static_pages_category",
            kwargs={"category_slug": self.slug})


TYPE_CHOICES = (
    (1, _(u'Foul copy')),
    (2, _(u'Published'))
)


class Page(models.Model):
    category = models.ManyToManyField(
        PageCategory,
        verbose_name=_(u"Category"))
    title = models.CharField(verbose_name=_(u"Title"), max_length=200)
    slug = models.SlugField(u"Slug", unique=True, max_length=200)
    icon = models.ImageField(
        verbose_name=_(u'Icon'),
        upload_to='scms_icons',
        null=True,
        blank=True
    )
    create_date = models.DateField(
        verbose_name=_(u"Create date"),
        default=datetime.today
    )
    active_date_start = models.DateField(
        verbose_name=_(u"Active date: start"),
        null=True,
        blank=True
    )
    active_date_stop = models.DateField(
        verbose_name=_(u"Active date: stop"),
        null=True,
        blank=True
    )
    show_on_full_site = models.BooleanField(
        verbose_name=_(u'Show on full site version'),
        default=True)
    show_on_mobile_site = models.BooleanField(
        verbose_name=_(u'Show on mobile site version'),
        default=True)
    type = models.IntegerField(
        choices=TYPE_CHOICES,
        verbose_name=_(u"Status"),
        default=1
    )
    template = models.CharField(
        choices=TEMPLATES,
        verbose_name=_(u"Template"),
        max_length=200,
        default="default.html"
    )
    vip = models.BooleanField(verbose_name=u"VIP")
    preamble = models.TextField(
        verbose_name=_(u"Preamble"),
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name=_(u"Body text")
    )
    position = models.PositiveIntegerField(
        verbose_name=_(u"Position"),
        null=True,
        blank=True,
        default=0
    )

    meta_title = models.TextField(_(u"Meta Title"), blank=True)
    meta_keywords = models.TextField(_(u"Meta Keywords"), blank=True)
    meta_description = models.TextField(_(u"Meta Description"), blank=True)
    meta_seo_text = models.TextField(_(u"Meta Text"), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _(u"Page")
        verbose_name_plural = _(u"Pages")

    def get_meta_title(self, request=None, context=None):
        data = {
            'name': self.title,
        }
        if self.meta_title != '':
            title = self.meta_title
        else:
            title = settings.SBITS_PAGES_META_TITLE
        return render_to_string(title, data)

    def get_meta_keywords(self, request=None, context=None):
        data = {
            'name': self.title,
        }
        if self.meta_keywords != '':
            meta_keywords = self.meta_keywords
        else:
            meta_keywords = settings.SBITS_PAGES_META_KEYWORDS
        return render_to_string(meta_keywords, data)

    def get_meta_description(self, request=None, context=None):
        data = {
            'name': self.title,
        }
        if self.meta_description != '':
            meta_description = self.meta_description
        else:
            meta_description = settings.SBITS_PAGES_META_DESCRIPTION
        return render_to_string(meta_description, data)

    def get_one_category(self):
        return self.category

    def get_absolute_url(self):
        return reverse(
            "static_pages_page",
            kwargs={
                "category_slug": self.category.all()[0].slug,
                "news_slug": self.slug
            }
        )
