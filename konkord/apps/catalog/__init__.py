from adminconfig import register
from .configurer import CatalogConfig


register(CatalogConfig)
default_app_config = 'catalog.apps.CatalogConfig'
