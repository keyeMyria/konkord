from .configurer import SearchConfig
from adminconfig import register

register(SearchConfig)

default_app_config = 'search.apps.SearchConfig'
