from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib.auth import authenticate, login


class UserQueryset(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

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

    def register_user(
            self, username, password, request, form_data, registration_fields):
        from .models import Email, Phone
        now = timezone.now()
        user_data = {
            'username': username,
            'is_staff': False,
            'is_active': True,
            'is_superuser': False,
            'last_login': now,
            'date_joined': now,
            'extra_data': {}
        }
        phone = None
        email = None
        for field in registration_fields:
            value = form_data.get(field['name'])
            if value:
                if field['name'] in ['first_name', 'last_name']:
                    user_data[field['name']] = value
                elif field['name'] == 'phone':
                    phone = value
                elif field['name'] == 'email':
                    email = value
                elif field['name'] == 'full_name':
                    splitted_full_name = value.strip().split(' ')
                    if len(splitted_full_name) == 2:
                        user_data['first_name'] = splitted_full_name[0]
                        user_data['last_name'] = splitted_full_name[1]
                    user_data['extra_data'][field['name']] = value
                else:
                    user_data['extra_data'][field['name']] = value
        user = self.model(**user_data)
        user.set_password(password)
        user.save()

        auth_by = getattr(settings, 'AUTHENTICATE_BY', 'email')
        if auth_by == 'email':
            Email.objects.create(
                email=user.username, default=True, user=user)
        else:
            Phone.objects.create(
                number=user.username, default=True, user=user)
        if phone:
            if auth_by == 'phone' and phone != user.username:
                Phone.objects.create(
                    number=phone, default=False, user=user)
            elif auth_by != 'phone':
                Phone.objects.create(
                    number=phone, default=True, user=user)
        if email:
            if auth_by == 'email' and email != user.username:
                Email.objects.create(
                    email=email, default=False, user=user)
            elif auth_by != 'email':
                Email.objects.create(
                    email=email, default=True, user=user)
        user = authenticate(username=username, password=password)
        login(request, user)
        return user

    def get_user(self, request, form_data):
        from .models import Email, Phone
        phone = form_data.get('phone')
        email = form_data.get('email')
        if request.user.is_authenticated():
            user = request.user
        else:
            query = Q()
            if email:
                query |= Q(emails__email=email)
            if phone:
                query |= Q(phones__number=phone)
            if not query:
                return None
            try:
                user = self.model.objects.distinct().get(query)
            except (
                    self.model.DoesNotExist,
                    self.model.MultipleObjectsReturned
            ):
                return None
        if email:
            Email.objects.get_or_create(email=email, user=user)
        if phone:
            Phone.objects.get_or_create(number=phone, user=user)
        return user
