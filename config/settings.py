# -*- coding: utf-8 -*-

'''
Django settings for ui project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
'''

import os

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG', False))

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# https://docs.djangoproject.com/en/dev/ref/settings/#append-slash
APPEND_SLASH = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'raven.contrib.django.raven_compat',
    'django.contrib.sessions',
    'config',
    'directory_header_footer',
    'directory_healthcheck',
    'health_check',
    'export_elements',
    'core',
    'directory_components',
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.api.v2',
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'modelcluster',
    'taggit',
    'rest_framework',
    'find_a_supplier.apps.FindASupplierConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.LocaleQuerystringMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'directory_header_footer.context_processors.urls_processor',
                'core.context_processors.feature_flags',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# # Database
# hard to get rid of this
DATABASES = {
    'default': dj_database_url.config()
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = (
    ('en-gb', 'English'),
    ('de', 'German'),
    ('ja', 'Japanese'),
    ('ru', 'Russian'),
    ('zh-hans', 'Simplified Chinese'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('pt', 'Portuguese'),
    ('pt-br', 'Portuguese (Brazilian)'),
    ('ar', 'Arabic'),
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = os.environ.get('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'mohawk': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'requests': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.SentryHandler'
                ),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


SIGNATURE_SECRET = os.environ['SIGNATURE_SECRET']

SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'true') == 'true'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '16070400'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# HEADER/FOOTER URLS
GREAT_EXPORT_HOME = os.getenv('GREAT_EXPORT_HOME')
GREAT_HOME = os.getenv('GREAT_HOME')
CUSTOM_PAGE = os.getenv('CUSTOM_PAGE')

# EXPORTING PERSONAS
EXPORTING_NEW = os.getenv('EXPORTING_NEW')
EXPORTING_REGULAR = os.getenv('EXPORTING_REGULAR')
EXPORTING_OCCASIONAL = os.getenv('EXPORTING_OCCASIONAL')

# GUIDANCE/ARTICLE SECTIONS
GUIDANCE_MARKET_RESEARCH = os.getenv('GUIDANCE_MARKET_RESEARCH')
GUIDANCE_CUSTOMER_INSIGHT = os.getenv('GUIDANCE_CUSTOMER_INSIGHT')
GUIDANCE_FINANCE = os.getenv('GUIDANCE_FINANCE')
GUIDANCE_BUSINESS_PLANNING = os.getenv('GUIDANCE_BUSINESS_PLANNING')
GUIDANCE_GETTING_PAID = os.getenv('GUIDANCE_GETTING_PAID')
GUIDANCE_OPERATIONS_AND_COMPLIANCE = os.getenv(
    'GUIDANCE_OPERATIONS_AND_COMPLIANCE')

# SERVICES
SERVICES_EXOPPS = os.getenv('SERVICES_EXOPPS')
SERVICES_EXOPPS_ACTUAL = os.getenv('SERVICES_EXOPPS_ACTUAL')
SERVICES_FAB = os.getenv('SERVICES_FAB')
SERVICES_GET_FINANCE = os.getenv('SERVICES_GET_FINANCE')
SERVICES_SOO = os.getenv('SERVICES_SOO')
SERVICES_EVENTS = os.getenv('SERVICES_EVENTS')

# FOOTER LINKS
INFO_ABOUT = os.getenv('INFO_ABOUT')
INFO_CONTACT_US_DIRECTORY = os.getenv('INFO_CONTACT_US_DIRECTORY')
INFO_PRIVACY_AND_COOKIES = os.getenv('INFO_PRIVACY_AND_COOKIES')
INFO_TERMS_AND_CONDITIONS = os.getenv('INFO_TERMS_AND_CONDITIONS')
INFO_DIT = os.getenv('INFO_DIT')

# Sentry
RAVEN_CONFIG = {
    'dsn': os.getenv('SENTRY_DSN'),
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'true') == 'true'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'true') == 'true'

# security
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Healthcheck
HEALTH_CHECK_TOKEN = os.environ['HEALTH_CHECK_TOKEN']

WAGTAIL_SITE_NAME = 'directory-cms'
BASE_URL = os.environ['BASE_URL']

# DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'config.signature.SignatureCheckPermission',
    ),
}

APP_URL_EXPORT_READINESS = os.environ['APP_URL_EXPORT_READINESS']
APP_URL_FIND_A_SUPPLIER = os.environ['APP_URL_FIND_A_SUPPLIER']

COPY_DESTINATION_URLS = os.environ['COPY_DESTINATION_URLS'].split(',')
