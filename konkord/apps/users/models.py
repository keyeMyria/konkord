# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name=_(u'Username'),
        max_length=255,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        verbose_name=_(u'First name'), max_length=255)
    last_name = models.CharField(verbose_name=_(u'Last name'), max_length=255)
    extra_data = JSONField(_(u'Extra data'), blank=True, null=True)

    objects = UserManager()

    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def email(self):
        email = self.emails.first()
        if email:
            return email.email
        return None

    @property
    def default_payment_method(self):
        if self.extra_data:
            return self.extra_data.get('payment_method')

    @default_payment_method.setter
    def default_payment_method(self, value):
        if not self.extra_data:
            self.extra_data = {}
        self.extra_data['payment_method'] = value

    @property
    def default_shipping_method(self):
        if self.extra_data:
            return self.extra_data.get('shipping_method')

    @default_shipping_method.setter
    def default_shipping_method(self, value):
        if not self.extra_data:
            self.extra_data = {}
        self.extra_data['shipping_method'] = value


class Phone(models.Model):
    number = models.CharField(verbose_name=_(u'Phone number'), max_length=30)
    user = models.ForeignKey(
        User, verbose_name=_(u'User'), related_name='phones')
    default = models.BooleanField(verbose_name=_(u'Default'), default=False)


class Email(models.Model):
    email = models.CharField(verbose_name=_(u'Email'), max_length=255)
    user = models.ForeignKey(
        User, verbose_name=_(u'User'), related_name='emails')
    default = models.BooleanField(verbose_name=_(u'Default'), default=False)
