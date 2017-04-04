from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    name = 'newsletter'

    def ready(self):
        from django.conf import settings
        from django.conf.urls import include, url
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'email',
            (
                'newsletter.Subscribe',
            )
        )
        settings.APPS_URLS.extend([
            url(r'^newsletter/', include('newsletter.urls'))
        ])