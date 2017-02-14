# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from catalog.models import Product
from search.utils import exclude_special_symbols


class SearchText(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(u'Product'))
    search_text = models.CharField(_(u'Search text'), max_length=512)

    def __str__(self):
        return self.product.name


def create_search_text(sender, **kwargs):
    product = kwargs['instance']
    try:
        search_text = SearchText.objects.get(product=product)
        search_text.search_text = exclude_special_symbols(product.name)
        search_text.save()
    except SearchText.DoesNotExist:
        SearchText.objects.create(
            product=product,
            search_text=exclude_special_symbols(product.name)
        )


post_save.connect(create_search_text, sender=Product)
