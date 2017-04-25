# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.conf import settings


def site(request):
    logo_url = settings.SITE_LOGO['url']
    return {
        'site': Site.objects.get_current(request),
        'logo_url': logo_url,
        'site_currency': settings.DEFAULT_CURRENCY
    }
