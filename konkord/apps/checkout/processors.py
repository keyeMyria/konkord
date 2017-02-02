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

    user_password_length = 6
    
    password_mail_template =\
        'checkout/background_registration/password_mail.html'
    password_mail_subject = 'checkout/background_registration/subject.html'
    order_mail_template = 'checkout/order/mail.html'
    order_mail_subject = 'checkout/order/subject.html'
    
    def __init__(self, request, cart, checkout_form):
        self.request = request
        self.form = checkout_form
        self.cart = cart
    
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

    def send_password_mail(self, user, password):
        html = render_to_string(
            self.password_mail_template,
            {
                'user': user,
                'password': password
            }
        )
        to_email = self.form.cleaned_data.get('email')
        subject = render_to_string(
            self.password_mail_subject,
            {}
        )
        if to_email:
            send_email(subject=subject, text=html, html=html, to=[to_email])

    def background_registration(self):
        username = self.form.cleaned_data.get(
            getattr(settings, 'AUTHENTICATE_BY', 'email'))
        password = User.objects.make_random_password(self.user_password_length)
        user = User.objects.register_user(
            username, password,
            self.request,
            self.form.cleaned_data, settings.CHECKOUT_USER_FIELDS)
        self.send_password_mail(user, password)
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
        order.price += order.payment_method.get_price()
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
