# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        # email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


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
    extra_data = JSONField(_(u'Exta data'), blank=True, null=True)
    email = None

    objects = UserManager()

    REQUIRED_FIELDS = []


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
