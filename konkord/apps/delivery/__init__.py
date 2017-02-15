from adminconfig import register
from .configurer import DeliveryConfig
default_app_config = 'delivery.apps.DeliveryConfig'
register(DeliveryConfig)