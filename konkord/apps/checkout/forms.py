# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from users.validators import validate_phone
from users.models import Email, Phone
from .models import PaymentMethod, ShippingMethod, Order
from delivery.models import City
from codemirror.widgets import CodeMirrorTextarea
from mail.utils import send_email, render
from django.contrib.sites.models import Site
from django.utils.translation import activate
from users.models import User
from suit_ckeditor.widgets import CKEditorWidget
from django.db.models import Q


class CheckoutForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for field in settings.CHECKOUT_USER_FIELDS:
            self.fields[field['name']] = getattr(forms, field['class'])(
                label=field['label'], required=field['required'])
        payment_methods = PaymentMethod.objects.filter(active=True)
        initial_payment_method = None
        initial_shipping_method = None
        user = self.request.user
        if user.is_authenticated():
            initial_payment_method = user.default_payment_method
            initial_shipping_method = user.default_shipping_method
        if payment_methods:
            self.fields['payment_method'] = forms.ModelChoiceField(
                label=_('Payment method'),
                queryset=payment_methods,
                required=True,
                initial=initial_payment_method
            )
        shipping_methods = ShippingMethod.objects.filter(active=True)
        if shipping_methods:
            self.fields['shipping_method'] = forms.ModelChoiceField(
                label=_('Shipping service'),
                queryset=shipping_methods,
                required=True,
                initial=initial_shipping_method
            )
            method_id = kwargs.get('data', {}).get(
                'shipping_method',
                self.initial.get('shipping_method', initial_shipping_method))
            city_id = kwargs.get('data', {})\
                .get('city', self.initial.get('city'))
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
        self.fields['user_message'] = forms.CharField(
            label=_('Message'),
            required=False,
            widget=forms.Textarea(
                attrs={'placeholder': _('Your message to us')})
        )
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
            if phone:
                self.fields['phone'].initial = phone.number
        if 'first_name' in self.fields:
            self.fields['first_name'].initial = self.request.user.first_name
        if 'last_name' in self.fields:
            self.fields['last_name'].initial = self.request.user.last_name
        if 'full_name' in self.fields:
            self.fields['full_name'].initial \
                = f'{self.request.user.first_name}'\
                f' {self.request.user.last_name}'

    def _validate_email(self, email):
        validate_email(email)
        try:
            if self.request.user.is_authenticated():
                Email.objects.exclude(
                    user=self.request.user).get(email=email)
                raise forms.ValidationError(_(u'Email taken by another user'))
        except Email.DoesNotExist:
            pass
        return email

    def _validate_phone(self, phone):
        number = validate_phone(phone)
        try:
            if self.request.user.is_authenticated():
                Phone.objects.exclude(
                    user=self.request.user).get(number=number)
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

    def clean(self):
        cleaned_data = super(CheckoutForm, self).clean()
        if not self.request.user.is_authenticated():
            phone = cleaned_data.get('phone')
            email = cleaned_data.get('email')
            if phone and email:
                users_count = User.objects.filter(
                    Q(phones__number=phone) | Q(emails__email=email)
                ).distinct().count()
                if users_count > 1:
                    if getattr(settings, 'AUTHENTICATE_BY', 'email'):
                        self.add_error(
                            'phone', _('Already taken by another user'))
                    else:
                        self.add_error(
                            'email', _('Already taken by another user'))
        return cleaned_data


class OrderAdminForm(forms.ModelForm):

    change_mail_template = 'checkout/order/change_mail_template.html'
    change_mail_subject = 'checkout/order/change_mail_subject.html'

    message = forms.CharField(
        label=_('Message'), widget=CKEditorWidget, required=False)

    class Meta:
        fields = '__all__'
        model = Order

    def send_mail(self, **kwargs):
        to_email = self.instance.user.email
        site = Site.objects.get_current()
        kwargs['site'] = site
        subject = render(
            self.change_mail_subject,
            **kwargs
        )
        html = render(
            self.change_mail_template,
            **kwargs
        )
        if to_email:
            send_email(subject=subject, text=html, html=html, to=[to_email])

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        obj = super(OrderAdminForm, self).save(commit)
        message_data = {}
        if 'status' in self.changed_data:
            message_data['status'] = cleaned_data['status']
        if 'message' in self.changed_data and cleaned_data['message']:
            message_data['message'] = cleaned_data['message']
        if message_data:
            activate(obj.language)
            message_data['order'] = obj
            self.send_mail(**message_data)
        return obj
