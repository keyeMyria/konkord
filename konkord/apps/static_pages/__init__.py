from adminconfig import register
from .configurer import StaticPagesConfig


register(StaticPagesConfig)

default_app_config = 'static_pages.apps.StaticPagesConfig'
