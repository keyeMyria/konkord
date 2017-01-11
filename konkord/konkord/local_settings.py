# -*- coding: utf-8 -*-
from konkord.settings import *


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

MEDIA_ROOT = os.path.join(BASE_DIR, "media"),
