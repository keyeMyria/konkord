from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib.sites.models import Site
        from django.conf import settings
        if not hasattr(settings, 'SITE_ID'):
            site = Site.objects.first()
            if not site:
                site = Site.objects.create(domain='example.com')
            settings.SITE_ID = site.id
