# -*- coding: utf-8 -*-
from django.db import models


class FilterOptionQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(products_count=0)


class FilterOptionManager(models.Manager):
    def get_queryset(self):
        return FilterOptionQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
