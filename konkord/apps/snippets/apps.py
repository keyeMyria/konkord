from django.apps import AppConfig


class SnippetsConfig(AppConfig):
    name = 'snippets'

    def ready(self):
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'static-content',
            (
                'snippets.Snippet',
            )
        )