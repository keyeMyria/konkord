from django.apps import AppConfig


class ComparisonConfig(AppConfig):
    name = 'comparison'

    def ready(self):
        from django.conf import settings
        from django.conf.urls import include, url
        settings.APPS_URLS.extend([
            url(r'^comparison/', include('comparison.urls'))
        ])