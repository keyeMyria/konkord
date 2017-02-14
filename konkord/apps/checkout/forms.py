# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from users.validators import validate_phone
from users.models import Email, Phone
from .models import PaymentMethod, ShippingMethod, Order
from delivery.models import City


class CheckoutForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for field in settings.CHECKOUT_USER_FIELDS:
            self.fields[field['name']] = getattr(forms, field['class'])(
                label=field['label'], required=field['required'])
        payment_methods = PaymentMethod.objects.filter(active=True)
        if payment_methods:
            self.fields['payment_method'] = forms.ModelChoiceField(
                label=_('Payment method'),
                queryset=payment_methods,
                required=True
            )
        shipping_methods = ShippingMethod.objects.filter(active=True)
        if shipping_methods:
            self.fields['shipping_method'] = forms.ModelChoiceField(
                label=_('Shipping method'),
                queryset=shipping_methods,
                required=True
            )
            method_id = kwargs.get('data', {}).get(
                'shipping_method', self.initial.get('shipping_method'))
            city_id = kwargs.get('data', {}).get('city', self.initial.get('city'))
            if method_id:
                try:
                    method = ShippingMethod.objects.exclude(
                        delivery_service=None).get(id=method_id)
                    cities = method.delivery_service.service.cities.filter(
                        active=True)
                    self.fields['city'] = forms.ModelChoiceField(
                        label=_('City'),
                        queryset=cities,
                        required=True
                    )
                except:
                    pass
            if method_id and city_id:
                try:
                    city = City.objects.get(
                        delivery_service__deliveryservicerelation__shipping_method__id=method_id,
                        id=city_id,
                        active=True
                    )
                    self.fields['office'] = forms.ModelChoiceField(
                        label=_('Office'),
                        queryset=city.offices.filter(active=True),
                        required=True
                    )
                except:
                    pass

        if self.request.user.is_authenticated():
            self.fill_initial_user_data()
    
    def fill_initial_user_data(self):
        if 'email' in self.fields:
            email = Email.objects.filter(
                user=self.request.user).order_by('-default').first()
            if email:
                self.fields['email'].initial = email.email
        if 'phone' in self.fields:
            phone = Phone.objects.filter(
                user=self.request.user).order_by('-default').first()
            if email:
                self.fields['phone'].initial = phone.number
        if 'first_name' in self.fields:
            self.fields['first_name'].initial = self.request.user.first_name
        if 'last_name' in self.fields:
            self.fields['last_name'].initial = self.request.user.last_name
        if 'full_name' in self.fields:
            self.fields['full_name'].initial \
                = f'{self.request.user.first_name}' \
                f' {self.request.user.last_name}'

    def _validate_email(self, email):
        validate_email(email)
        if getattr(settings, 'AUTHENTICATE_BY', 'email') == 'phone':
            try:
                if self.request.user.is_authenticated():
                    Email.objects.exclude(
                        user=self.request.user).get(email=email)
                else:
                    Email.objects.exclude(
                        user__phones__number=self.cleaned_data.get('phone')
                    ).get(email=email)
                raise forms.ValidationError(_(u'Email taken by another user'))
            except Email.DoesNotExist:
                pass

    def _validate_phone(self, phone):
        number = validate_phone(phone)
        if getattr(settings, 'AUTHENTICATE_BY', 'email') == 'email':
            try:
                if self.request.user.is_authenticated():
                    Phone.objects.exclude(
                        user=self.request.user).get(number=number)
                else:
                    Phone.objects.exclude(
                        user__emails__email=self.cleaned_data.get('email')
                    ).get(number=number)
                raise forms.ValidationError(
                    _(u'This number taken by another user')
                )
            except Phone.DoesNotExist:
                pass
        return number

    def clean_email(self):
        email = self.cleaned_data['email']
        self._validate_email(email)
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = self._validate_phone(phone)
        return phone


class OrderAdminForm(forms.ModelForm):
    
    class Meta:
        fields = '__all__'
        model = Order
    
    def __init__(self, *args, **kwargs):
        super(OrderAdminForm, self).__init__(*args, **kwargs)