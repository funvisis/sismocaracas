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

MEDIA_ROOT = os.path.join(MY_PROJECT_PATH, '..', 'media', 'sismocaracas')
DJANGO_PROJECTS_PATH = '/home/danielmaxx/work/FUNVISIS'
MY_PROJECT_PATH = os.path.join(DJANGO_PROJECTS_PATH, PROJECT_NAME)

MEDIA_ROOT = os.path.join(MY_PROJECT_PATH, 'media/')
MEDIA_URL = '/media/' 
ADMIN_MEDIA_PREFIX='/static/admin/'

STATIC_ROOT = ''#'"os.path.join(MY_PROJECT_PATH, 'media/')
STATIC_URL = '/static/'
ADMIN_STATIC_PREFIX='/static/admin/'
STATICFILES_DIRS = ()

TEMPLATE_DIRS = (os.path.join(os.getcwd(), 'templates'))
