# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.conf import settings


def site(request):
    if settings.MEDIA_ROOT in settings.SITE_LOGO:
        logo_url = settings.MEDIA_URL + settings.SITE_LOGO.split(
            settings.MEDIA_ROOT)[-1]
    else:
        logo_url = settings.SITE_LOGO
    return {
        'site': Site.objects.get_current(request),
        'logo_url': logo_url
    }
