from adminconfig import register
from .configurer import CoreConfig

register(CoreConfig)
print('core')
default_app_config = 'core.apps.CoreConfig'
