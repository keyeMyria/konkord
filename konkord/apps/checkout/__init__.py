from adminconfig import register
from .configurer import CheckoutJobsConfig

register(CheckoutJobsConfig)

default_app_config = 'checkout.apps.CheckoutConfig'


