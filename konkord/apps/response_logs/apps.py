from django.apps import AppConfig


class ResponseLogsConfig(AppConfig):
    name = 'response_logs'

    def ready(self):
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'reports',
            (
                'response_logs.ResponseLog',
            )
        )