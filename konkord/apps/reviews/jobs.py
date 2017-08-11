# coding: utf-8
from mail.utils import send_email, render
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import activate


def review_product_mail_job(*args, **kwargs):
    from checkout.models import Order
    order = Order.objects.get(id=kwargs['order_id'])
    activate(order.language)
    subject = render(
        'review_products/subject.html'
    )
    email = order.get_user_email()
    if settings.MEDIA_ROOT in settings.SITE_LOGO:
        logo_url = settings.MEDIA_URL + settings.SITE_LOGO.split(
            settings.MEDIA_ROOT)[-1]
    else:
        logo_url = settings.SITE_LOGO
    data = {
        'order': order,
        'host': Site.objects.get_current(),
        'logo': logo_url
    }
    html = render(
        'review_products/mail.html',
        **data
    )
    if email:
        send_email(subject, '', [email], html)
