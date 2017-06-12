from django.apps import AppConfig


class ResponseLogsConfig(AppConfig):
    name = 'response_logs'

    def ready(self):
        from django.conf import settings
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'reports',
            (
                'response_logs.ResponseLog',
            )
        )
        settings.MIDDLEWARE = [
            'response_logs.middleware.ResponseLogMiddleware'
        ] + settings.MIDDLEWARE
