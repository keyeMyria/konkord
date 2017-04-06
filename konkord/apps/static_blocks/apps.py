from django.apps import AppConfig


class StaticBlocksConfig(AppConfig):
    name = 'static_blocks'

    def ready(self):
        from core import add_to_suit_config_menu
        add_to_suit_config_menu(
            'static-content',
            (
                'static_blocks.StaticBlock',
            )
        )