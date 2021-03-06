"""
Django settings for konkord project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

ugettext = lambda s: s

gettext = lambda s: s


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(0, APPS_DIR)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1*0c%3vx(3#)99bveov*u1y8!-w8yl7ql1+fq*c=3_f2^u+n5@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'basic_theme',
    'adminconfig',
    'core',
    'konkord',
    'dal',
    'dal_select2',
    'filer',
    'suit',
    'modeltranslation',
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'redirects',
    'django.contrib.sitemaps',
    'easy_thumbnails',
    'mptt',
    'robots',
    'genericadmin',
    'django_mptt_admin',
    'codemirror',
    'suit_ckeditor',
    'tasks',
    'django_rq',
    'scheduler',
    'search',
    'catalog',
    'suit_sortable',
    'filters',
    'bootstrap3',
    'snowpenguin.django.recaptcha2',
    'exchange',
    'checkout',
    'mail',
    'reviews',
    'static_pages',
    'pdf_pages',
    'delivery',
    'static_blocks',
    'newsletter',
    'compressor',
    'response_logs',
    'price_navigator',
    'comparison',
    'maintenance',
    'snippets',
    'seo'
]
# Application definition


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance.middleware.MaintenanceMiddleware',
    'core.middleware.LocaleMiddleware',
]

ROOT_URLCONF = 'konkord.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'core.context_processors.site',
                'search.context_processors.search'
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/stylus', 'stylus < {infile} > {outfile}'),
)

WSGI_APPLICATION = 'konkord.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

MEDIA_URL = '/media/'

APPS_URLS = []

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
}

LANGUAGES = [
    ('ru', gettext('Russian')),
    ('uk', gettext('Ukrainian')),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
SUIT_CONFIG = {
    'ADMIN_NAME': 'Konkord',
    'HEADER_DATE_FORMAT': 'l, j F Y',   # Saturday, 16 March 2013
    'HEADER_TIME_FORMAT': 'H:i',        # 18:42

    'MENU': (
        {
            'label': gettext('Users'),
            'icon': 'icon-user',
            'tag': 'users',
            'models': (),
        },
        {
            'label': gettext('Catalog'),
            'icon': 'icon-align-justify',
            'tag': 'catalog',
            'models': (),
        },
        {
            'label': gettext('Static content'),
            'icon': 'icon-file',
            'tag': 'static-content',
            'models': ()
        },
        {
            'label': gettext('Commerce'),
            'icon': 'icon-shopping-cart',
            'tag': 'commerce',
            'models': (),
        },
        {
            'label': gettext('Marketing'),
            'icon': 'icon-barcode',
            'tag': 'marketing',
            'models': (),
        },
        {
            'label': gettext('Delivery'),
            'icon': 'icon-globe',
            'tag': 'delivery',
            'models': (),
        },
        {
            'label': gettext('Email'),
            'icon': 'icon-envelope',
            'tag': 'email',
            'models': (),
        },
        {
            'label': gettext('Configuration'),
            'icon': 'icon-wrench',
            'tag': 'configuration',
            'models': (
                'redirects.Redirect',
                'sites.Site',
                'robots.Url',
                'robots.Rule'
            ),
        },
        {
            'label': gettext('Tasks'),
            'icon': 'icon-tasks',
            'tag': 'tasks',
            'models': (),
        },
        {
            'label': gettext('Exchange'),
            'icon': 'icon-download-alt',
            'tag': 'exchange',
            'models': (),
        },
        {
            'label': gettext('Reports and logs'),
            'icon': 'icon-flag',
            'tag': 'reports',
            'models': (),
        },
        {
            'label': gettext('Filer'),
            'icon': 'icon-file',
            'tag': 'filer',
            'models': (
                'filer.thumbnailoption',
                'filer.folder'
            )
        }
    )
}

from tasks.api import RQTaskQueue

ACTIVE_TASK_QUEUE = RQTaskQueue()

FROM_EMAIL = 'dev'
ORDER_NUMBER_PREFIX = ''

CODEMIRROR_THEME = 'neat'
SITE_ID = 1
GLOBAL_JSON_CONFIG = os.path.join(BASE_DIR, 'config.json')
SITE_PROTOCOL = 'http'


try:
    LOCAL_SETTINGS
except:
    from .local_settings import *
