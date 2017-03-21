# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel
from datetime import datetime
from .settings import TEMPLATES
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from seo.models import ModelWithSeoMixin


SORT_CHOICES = (
    (1, _(u'Direct')),
    (2, _(u'Reverse')),
)


class PageCategory(ModelWithSeoMixin, MPTTModel):
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

    # meta_title = models.TextField(_(u"Meta Title"), blank=True)
    # meta_keywords = models.TextField(_(u"Meta Keywords"), blank=True)
    # meta_description = models.TextField(_(u"Meta Description"), blank=True)
    # meta_seo_text = models.TextField(_(u"Meta Text"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Page category")
        verbose_name_plural = _(u"Pages categories")

    class MPTTMeta:
        order_insertion_by = ['name', ]


    def get_absolute_url(self):
        return reverse(
            "static_pages_category",
            kwargs={"slug": self.slug}, urlconf='static_pages.urls_i18n')


TYPE_CHOICES = (
    (1, _(u'Foul copy')),
    (2, _(u'Published'))
)


class Page(ModelWithSeoMixin, models.Model):
    category = models.ManyToManyField(
        PageCategory,
        verbose_name=_(u"Category"))
    title = models.CharField(verbose_name=_(u"Title"), max_length=200)
    slug = models.SlugField(u"Slug", unique=True, max_length=200)
    icon = models.ImageField(
        verbose_name=_(u'Icon'),
        upload_to='static_pages_icons',
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


    def get_one_category(self):
        return self.category

    def get_absolute_url(self):
        return reverse(
            "static_pages_page",
            kwargs={
                "category_slug": self.category.first().slug,
                "page_slug": self.slug
            }
        )
