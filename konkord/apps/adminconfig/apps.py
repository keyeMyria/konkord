from django.apps import AppConfig


class AdminConfigConfig(AppConfig):
    name = 'adminconfig'

    def ready(self):
        from django.conf import settings
        from core import add_to_suit_config_menu
        from .urls import urlpatterns
        from adminconfig.utils import JSONConfigFile
        from django.utils.translation import ugettext_lazy as _

        add_to_suit_config_menu(
            'configuration',
            (
                {'url': 'admin_config_index', 'label': _('Configuration')},
            )
        )

        settings.APPS_URLS.extend(urlpatterns)
        json_config = JSONConfigFile(settings.GLOBAL_JSON_CONFIG)
        json_config.get_full_config()
        for block_name in json_config.config.keys():
            block = json_config.config[block_name]
            for config_name, config_value in block.items():
                setattr(settings, config_name, config_value)
