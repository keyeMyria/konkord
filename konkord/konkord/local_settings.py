# -*- coding: utf-8 -*-
from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'konkord_yas',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
ALLOWED_HOSTS = ['*']
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# RECAPTCHA_PUBLIC_KEY = '6LczxwgUAAAAAEv44HwttJFXOzXAEp0ffAfBqM7V'
# RECAPTCHA_PRIVATE_KEY = '6LczxwgUAAAAABtJKEMwi3zT3bMuPAYVFgSRlr2u'

INSTALLED_APPS = ['yas_theme'] + INSTALLED_APPS

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         # 'LOCATION': 'unix:/tmp/memcached.sock',
#         'LOCATION': '127.0.0.1:11211',
#         'TIMEOUT': 2592000,
#         'KEY_PREFIX': 'infoshina',
#         # 'KEY_FUNCTION': hash_key,
#     }
# }