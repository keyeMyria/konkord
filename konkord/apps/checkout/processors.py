# -*- coding: utf-8 -*-
from .models import Order, OrderItem
from django.db.models import Q
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from users.models import User, Email, Phone
import string
import random
from mail.utils import send_email
from django.template.loader import render_to_string
from django.shortcuts import redirect, reverse


class BasePaymentProcessor(object):
    
    password_mail_template =\
        'checkout/background_registration/password_mail.html'
    password_mail_subject = 'checkout/background_registration/subject.html'
    order_mail_template = 'checkout/order/mail.html'
    order_mail_subject = 'checkout/order/subject.html'
    
    def __init__(self, request, cart, checkout_form):
        self.request = request
        self.form = checkout_form
        self.cart = cart

    @staticmethod
    def pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    def send_order_created_mail(self, order):
        to_email = self.form.cleaned_data.get('email')
        subject = render_to_string(
            self.order_mail_subject,
            {'order': order}
        )
        html = render_to_string(
            self.order_mail_template,
            {'order': order}
        )
        if to_email:
            send_email(subject=subject, text=html, html=html, to=[to_email])

    def send_password_mail(self, password):
        html = render_to_string(
            self.password_mail_template,
            {'password': password}
        )
        to_email = self.form.cleaned_data.get('email')
        subject = render_to_string(
            self.password_mail_subject,
            {}
        )
        if to_email:
            send_email(subject=subject, text=html, html=html, to=[to_email])

    def background_registration(self):
        now = timezone.now()
        username = self.form.cleaned_data.get(
            getattr(settings, 'AUTHENTICATE_BY', 'email'))
        password = self.pass_generator()
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
        for field in settings.CHECKOUT_USER_FIELDS:
            value = self.form.cleaned_data.get(field['name'])
            if value:
                if field['name'] in ['first_name', 'last_name']:
                    user_data[field['name']] = value
                elif field['name'] == 'phone':
                    phone = value
                elif field['name'] == 'email':
                    email = value
                elif field['name'] == 'full_name':
                    splitted_full_name = value.split(' ')
                    if len(splitted_full_name) == 2:
                        user_data['first_name'] = splitted_full_name[0]
                        user_data['last_name'] = splitted_full_name[1]
                    user_data['extra_data'][field['name']] = value
                else:
                    user_data['extra_data'][field['name']] = value
        user = User(**user_data)
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
        return user

    def get_user(self):
        if self.request.user.is_authenticated():
            user = self.request.user
        else:
            try:
                auth_by = getattr(settings, 'AUTHENTICATE_BY', 'email')
                if auth_by == 'email':
                    user = User.objects.get(
                        emails__email=self.form.cleaned_data[auth_by])
                else:
                    user = User.objects.get(
                        phones_number=self.form.cleaned_data[auth_by])
            except User.DoesNotExist:
                return self.background_registration()
        email = self.form.cleaned_data.get('email')
        phone = self.form.cleaned_data.get('phone')
        if email:
            Email.objects.get_or_create(email=email, user=user)
        if phone:
            Phone.objects.get_or_create(number=phone, user=user)
        return user

    @transaction.atomic
    def process(self):
        order = Order.objects.create(
            user=self.get_user(),
            status=Order.get_default_status(),
            payment_method=self.form.cleaned_data.get('payment_method'),
        )
        order.price += order.payment_method.price
        for cart_item in self.cart.items.all():
            order.items.create(
                product=cart_item.product,
                product_amount=cart_item.amount,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price
            )
            order.price += cart_item.product.price * cart_item.amount
        order.save()
        self.cart.delete()
        self.request.session['order_id'] = order.id
        self.send_order_created_mail(order)
        return redirect(reverse('thank_you_page'))
