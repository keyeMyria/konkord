from adminconfig import register
from .configurer import CheckoutJobsConfig, CheckoutConfig


register(CheckoutJobsConfig)
register(CheckoutConfig)

default_app_config = 'checkout.apps.CheckoutConfig'
