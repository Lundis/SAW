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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r8j^!ps$%c#!lt7y(vb%o&r-dxk&qghp3k%ga=ngz#4p5ayr_u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

EXTERNAL_APPS = (
    'solo', # singleton models. pip install django-solo
    'bootstrap3', # bootstrap templates
)

NON_OPTIONAL_APPS = (
    'base',
    'members',
    'theme',
    'menu',
    'install',
    'users',
    'settings',
)

OPTIONAL_APPS = ()

# Load non-critical modules dynamically
# http://stackoverflow.com/questions/24027901/dynamically-loading-django-apps-at-runtime

for app in get_all_modules():
    if app not in NON_OPTIONAL_APPS:
        # make sure we don't load this (studassweb) module as an app
        if app != __package__:
            OPTIONAL_APPS += (app, )

# Application definition, list all built-in apps here
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
) + EXTERNAL_APPS + NON_OPTIONAL_APPS + OPTIONAL_APPS



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'studassweb.urls'

WSGI_APPLICATION = 'studassweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/users/login/'