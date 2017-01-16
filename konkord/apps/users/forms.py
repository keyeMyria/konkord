# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from users.validators import validate_phone
from users.models import Email, Phone, User
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=getattr(settings, 'USER_USERNAME_LABEL', _(u'Username')),
    )
    password_1 = forms.CharField(
        label=_(u'Password'), widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label=_(u'Confirm password'), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in settings.REGISTER_FIELDS:
            self.fields[field['name']] = getattr(forms, field['class'])(
                label=field['label'], required=field['required'])
        if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and\
                hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
            self.fields['captcha'] = ReCaptchaField(
                widget=ReCaptchaWidget(), label=_(u'Captcha'))
        self.fields.move_to_end('password_1')
        self.fields.move_to_end('password_2')

    def clean_password_2(self):
        """Validates that password 1 and password 2 are the same.
        """
        p1 = self.cleaned_data.get('password_1')
        p2 = self.cleaned_data.get('password_2')

        if not (p1 and p2 and p1 == p2):
            raise forms.ValidationError(_(u"The two passwords do not match."))

        return p2

    def _validate_email(self, email):
        validate_email(email)
        try:
            Email.objects.get(email=email)
            raise forms.ValidationError(_(u'Email alredy exists'))
        except Email.DoesNotExist:
            pass

    def _validate_phone(self, phone):
        number = validate_phone(phone)
        try:
            Phone.objects.get(number=number)
            raise forms.ValidationError(
                _(u'This %s number already exists' % number)
            )
        except Phone.DoesNotExist:
            pass
        return number

    def clean_username(self):
        username = self.cleaned_data['username']
        if getattr(settings, 'AUTHENTICATE_BY', 'email') == 'email':
            self._validate_email(username)
        else:
            username = self._validate_phone(username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        self._validate_email(email)
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = self._validate_phone(phone)
        return phone


class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if getattr(settings, 'AUTHENTICATE_BY', 'email') == 'email':
            validate_email(username)
        else:
            username = validate_phone(username)
        return username


class UserResetPasswordForm(PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = User._default_manager.filter(
            emails__email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        try:
            Email.objects.get(email=email)
        except Email.DoesNotExist:
            raise forms.ValidationError(_(u'Email is not register'))
