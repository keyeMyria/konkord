# -*- coding: utf-8 -*-
from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'konkord',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

RECAPTCHA_PUBLIC_KEY = '6LczxwgUAAAAAEv44HwttJFXOzXAEp0ffAfBqM7V'
RECAPTCHA_PRIVATE_KEY = '6LczxwgUAAAAABtJKEMwi3zT3bMuPAYVFgSRlr2u'
