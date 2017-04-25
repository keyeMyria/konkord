from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    name = 'maintenance'

    def ready(self):
        from django.conf import settings
        from core import add_to_suit_config_menu
        from django.conf.urls import url, include

        add_to_suit_config_menu(
            'configuration',
            (
                'maintenance.MaintenanceMessage',
            )
        )

        settings.APPS_URLS.extend([
            url(r'^maintenance/', include('maintenance.urls'))
        ])
