# -*- coding: utf-8 -*-

from settings_base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',}}

# MEDIA_ROOT = os.path.join(MY_PROJECT_PATH, '..', 'media', 'sismocaracas')
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX='/static/admin/'

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()

TEMPLATE_DIRS = (os.path.join(os.getcwd(), 'templates'))

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar')

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)
