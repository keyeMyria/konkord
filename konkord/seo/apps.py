from django.apps import AppConfig


class SeoConfig(AppConfig):
    name = 'seo'

    def ready(self):
        from core import add_to_suit_config_menu

        add_to_suit_config_menu(
            'marketing',
            (
                'seo.SEOForPage',
            )
        )
