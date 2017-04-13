# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from catalog.models import Product
from search.utils import exclude_special_symbols
from django.conf import settings


class SearchText(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(u'Product'))
    search_text = models.CharField(_(u'Search text'), max_length=512)

    def __str__(self):
        return self.product.name


def create_search_text(sender, **kwargs):
    product = kwargs['instance']
    try:
        search_text = SearchText.objects.get(product=product)
        for language in settings.LANGUAGES:
            setattr(
                search_text,
                f'search_text_{language[0]}',
                exclude_special_symbols(
                    getattr(product, f'name_{language[0]}')
                )
            )
    except SearchText.DoesNotExist:
        search_text = SearchText.objects.create(
            product=product,
        )
        for language in settings.LANGUAGES:
            setattr(
                search_text,
                f'search_text_{language[0]}',
                exclude_special_symbols(
                    getattr(product, f'name_{language[0]}')
                )
            )
    search_text.save()


post_save.connect(create_search_text, sender=Product)
