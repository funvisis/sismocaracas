# -*- coding: utf-8 -*-
from settings_base import *

# ==================================
# Variables propia de proyectos FVIS
# ==================================
# Válidas en producción.
# TODO: Documentar

PROJECT_NAME = 'sismocaracas'
DJANGO_PROJECTS_PATH = '/usr/lib/django-projects'
MY_PROJECT_PATH = os.path.join(DJANGO_PROJECTS_PATH, PROJECT_NAME)


# ===================== 
# Configuración clásica
# =====================

DEBUG = False
TEMPLATE_DEBUG = False


ADMINS = (
    ('admunix', 'admunix@funvisis.gob.ve'),
)

MANAGERS = (
    ('admunix', 'admunix@funvisis.gob.ve'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_sismocaracas',
        'USER': 'sismocaracas_user',
        'PASSWORD': 'jojoto',
        'HOST': 'db.funvisis.gob.ve',
        'PORT': '5432',
    }
}

MEDIA_ROOT = os.path.join('/', 'sdb', 'www', 'sismocaracasst',  PROJECT_NAME, 'media')
MEDIA_URL = 'http://sismocaracasst/' + PROJECT_NAME + '/media/'
STATIC_ROOT = os.path.join('/sdb/www/sismocaracasst', PROJECT_NAME)
STATIC_URL = 'http://sismocaracasst/' + PROJECT_NAME + '/'
ADMIN_MEDIA_PREFIX = 'http://sismocaracasst/' + PROJECT_NAME + '/admin/'

STATICFILES_DIRS = ()

TEMPLATE_DIRS = (os.path.join(os.getcwd(), 'templates'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
