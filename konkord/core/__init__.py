from adminconfig import register
from .configurer import CoreConfig
from .utils import add_to_suit_config_menu

register(CoreConfig)
default_app_config = 'core.apps.CoreConfig'


__all__ = ['add_to_suit_config_menu']
