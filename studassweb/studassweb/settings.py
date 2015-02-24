"""
Django settings for studassweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from base.utils import get_all_modules

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

EXTERNAL_APPS = (
    'solo',  # singleton models. pip install django-solo
    'bootstrap3',  # bootstrap templates
    'ckeditor',
    'easy_thumbnails',  # you need to run "python manage.py migrate easy_thumbnails" after installing
    'captcha',
    'django_ajax',
)

NON_OPTIONAL_APPS = (
    'base',
    'members',
    'menu',
    'install',
    'users',
    'settings',
    'frontpage',
)

OPTIONAL_APPS = ()


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'studassweb.middleware.VerifyModuleEnabled',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'studassweb.urls'

WSGI_APPLICATION = 'studassweb.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

LOGIN_URL = '/users/login/'

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_URL = '/media/'

# wysiwyg editor files will be uploaded to MEDIA_ROOT/CKEDITOR_UPLOAD_PATH
CKEDITOR_UPLOAD_PATH = "ckeditor/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
    },
}


THUMBNAIL_BASEDIR = "thumbnails"


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# Default no-reply to use.
NO_REPLY_EMAIL = "noreply@localhost"

#The directory in which log files should be created
LOG_DIR = os.path.join(os.path.dirname(SITE_ROOT), 'logs')

# load local settings
exec(open(os.path.join(os.path.dirname(__file__), 'settings_local.py')).read(), globals())

# Set up static file serving
if STATIC_DJANGO:
    STATICFILES_DIRS = (
        STATIC_DIR,
    )
else:
    # We are using an external static file server such as apache.
    STATIC_ROOT = STATIC_DIR

# Load non-critical modules dynamically
# http://stackoverflow.com/questions/24027901/dynamically-loading-django-apps-at-runtime
# load this after local settings due to dependencies
for app in get_all_modules():
    if app not in NON_OPTIONAL_APPS:
        # make sure we don't load this (studassweb) module as an app
        if app != __package__:
            OPTIONAL_APPS += (app, )

# Application definition, list all built-in apps here
INSTALLED_APPS += EXTERNAL_APPS + NON_OPTIONAL_APPS + OPTIONAL_APPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
        'simple': {
            'format': '%(levelname)s [%(name)s:%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'djangodebugfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'djangodebug.log'),
            'formatter': 'verbose'
        },
        'appdebugfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'appdebug.log'),
            'formatter': 'verbose'
        },
        'allwarnings': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'allwarnings.log'),
            'formatter': 'verbose'
        },
        'console-warnings': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['djangodebugfile', 'allwarnings', 'console-warnings'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'studassweb': {
            'handlers': ['appdebugfile', 'allwarnings'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

if DEBUG:
    LOGGING['handlers']['console'] = {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'}
    LOGGING['loggers']['studassweb']['handlers'].append('console')

#This is the logger added to every module
if DEBUG:
    local_logger_conf = {
        'handlers': ['allwarnings', 'appdebugfile', 'console'],
        'level': 'DEBUG',
        'propagate': True,
    }
else:
    local_logger_conf = {
        'handlers': ['allwarnings', 'appdebugfile'],
        'level': 'DEBUG',
        'propagate': True,
    }

#Add to every module
for app in get_all_modules():
    LOGGING['loggers'][app] = local_logger_conf

#This makes django messages compatible with bootstrap3
#http://ericsaupe.com/tag/bootstrap-messages-fix/
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger'}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'