# -*- coding: utf-8 -*-
from django.db import models


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def in_search(self):
        return self.active().filter(status__in_search=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def in_search(self):
        return self.active().in_search()
