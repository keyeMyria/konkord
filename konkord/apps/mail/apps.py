from django.apps import AppConfig


class MailConfig(AppConfig):
    name = 'mail'

    def ready(self):
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'email',
            (
                'mail.MailTemplate',
            )
        )