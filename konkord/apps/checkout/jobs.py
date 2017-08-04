# coding: utf-8
from mail.utils import send_email, render
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import activate

task_manager = settings.ACTIVE_TASK_QUEUE


def forgotten_cart_send_email_job(*args, **kwargs):
    from .models import Cart
    from datetime import timedelta, datetime, timezone

    cart_id = None
    try:
        cart = Cart.objects.get(id=kwargs['cart_id'])
        if cart.updated.strftime("%Y-%m-%d %H:%M:%S.%f%z") !=\
                kwargs['cart_modification_date'] and not kwargs.get('debug'):
            cart = None
        else:
            cart_id = cart.id
    except:
        cart = None
    if cart is not None and cart.user is not None and cart.items.exists():
        activate(cart.language)
        subject = render(
            'checkout/forgotten_cart/forgotten_cart_mail_subject.html'
        )
        email = cart.user.email
        if settings.MEDIA_ROOT in settings.SITE_LOGO:
            logo_url = settings.MEDIA_URL + settings.SITE_LOGO.split(
                settings.MEDIA_ROOT)[-1]
        else:
            logo_url = settings.SITE_LOGO
        data = {
            'cart': cart,
            'host': Site.objects.get(id=settings.SITE_ID),
            'logo': logo_url
        }
        html = render(
            'checkout/forgotten_cart/forgotten_cart_mail.html',
            **data
            )
        send_email(subject, '', [email], html)
    mod_date = datetime.strptime(
        kwargs['cart_modification_date'], "%Y-%m-%d %H:%M:%S.%f%z")
    cart_for_send_mail = Cart.objects.filter(
        updated__gt=mod_date,
        ).exclude(id=cart_id).order_by('updated').first()
    if cart_for_send_mail and kwargs['run_after'] in\
            settings.CART_CHANGED_EMAIL_SEND_AFTER.split(','):
        modification_date = cart_for_send_mail.updated
        task_manager.schedule(
            'checkout.jobs.forgotten_cart_send_email_job',
            kwargs={
                'cart_modification_date': modification_date.strftime(
                    "%Y-%m-%d %H:%M:%S.%f%z"),
                'cart_id': cart_for_send_mail.id,
                'run_after': kwargs['run_after']
                },
            run_after=modification_date.replace(
                tzinfo=timezone.utc
            ).astimezone(tz=None) + timedelta(
                minutes=int(kwargs['run_after'])
            )
        )
