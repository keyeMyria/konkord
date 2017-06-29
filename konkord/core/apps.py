from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core import add_to_suit_config_menu
        from django.utils.translation import ugettext_lazy as _
        add_to_suit_config_menu(
            'configuration',
            (
                {
                    'url': '/admin/redirects/redirect/redirects_import/',
                    'label': _('Redirects import')
                },
            )
        )