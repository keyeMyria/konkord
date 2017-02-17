from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    name = 'newsletter'

    def ready(self):
        from django.conf import settings
        from django.conf.urls import include, url
        settings.APPS_URLS.extend([
            url(r'^newsletter/', include('newsletter.urls'))
        ])