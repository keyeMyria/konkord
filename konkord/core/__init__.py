from adminconfig import register
from .configurer import CoreConfig

register(CoreConfig)
default_app_config = 'core.apps.CoreConfig'
