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

    class Meta:
        verbose_name = _('Search text')
        verbose_name_plural = _('Search texts')

    def save(self, *args, **kwargs):
        for language in settings.LANGUAGES:
            search_text = getattr(self, f'search_text_{language[0]}')
            setattr(
                self,
                f'search_text_{language[0]}',
                exclude_special_symbols(search_text))
        super(SearchText, self).save(*args, **kwargs)


def create_search_text(sender, **kwargs):
    product = kwargs['instance']
    kwargs = {}
    for language in settings.LANGUAGES:
        kwargs[f'search_text_{language[0]}'] = exclude_special_symbols(
            getattr(product, f'name_{language[0]}')
        )
    if not SearchText.objects.filter(product=product, **kwargs).exists():
        SearchText.objects.create(product=product, **kwargs)
    # if not SearchText.objects.filter(product=product).exists():
        # search_text = SearchText.objects.create(
        #     product=product,
        # )
            #     search_text,
            #     f'search_text_{language[0]}',
                
            # )
    # search_text.save()


post_save.connect(create_search_text, sender=Product)
