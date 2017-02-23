# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q


class CartQuerySet(models.QuerySet):
    def get_user_cart(self, request):
        return self.get(
                Q(user=request.user) if request.user.is_authenticated() else
                Q(session=request.session.session_key)
            )


class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)

    def get_user_cart(self, request):
        return self.get_queryset().get_user_cart(request)
