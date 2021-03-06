# -*- coding: utf-8 -*-
from django.db import models
from .settings import PRODUCT_WITH_VARIANTS, VARIANT


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def in_search(self):
        return self.active().filter(status__in_search=True)

    def with_variants(self):
        return self.active().filter(product_type=PRODUCT_WITH_VARIANTS)

    def variants(self):
        return self.active().filter(product_type=VARIANT)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def in_search(self):
        return self.get_queryset().in_search()

    def with_variants(self):
        return self.get_queryset().with_variants()

    def variants(self):
        return self.get_queryset().variants()
