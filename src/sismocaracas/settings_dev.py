# -*- coding: utf-8 -*-

from settings_base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
     'default': {
         'ENGINE': 'django.contrib.gis.db.backends.spatialite',
         'NAME': 'db.sqlite3',
         'USER': '',
         'PASSWORD': '',
         'HOST': '',
         'PORT': '',}
    #'default': {
    #    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #    'NAME': 'geodjango',
    #    'USER': 'geo',
    #    'PASSWORD': 'geo',
    #    'HOST': '',
    #    'PORT': '',}
    }

MEDIA_ROOT = os.path.join(MY_PROJECT_PATH, '..', 'media', 'sismocaracas')
DJANGO_PROJECTS_PATH = os.getcwd()
MY_PROJECT_PATH = os.path.join(DJANGO_PROJECTS_PATH, PROJECT_NAME)

MEDIA_ROOT = os.path.join(MY_PROJECT_PATH, 'media/')
MEDIA_URL = '/static/media/' 
ADMIN_MEDIA_PREFIX='/static/admin/'

STATIC_ROOT = ''#'"os.path.join(MY_PROJECT_PATH, 'media/')
STATIC_URL = '/static/'
ADMIN_STATIC_PREFIX='/static/admin/'
STATICFILES_DIRS = (
    MY_PROJECT_PATH,
)

TEMPLATE_DIRS = (os.path.join(os.getcwd(), 'templates'))

#from sismocaracas.structuralinspections.utils import get_image_path
#PHOTOLOGUE_PATH = get_image_path

#from sismocaracas.structuralinspections.utils import get_sample_image_path
SAMPLE_IMAGE_PATH = os.path.join(MEDIA_ROOT, 'photologue/samples/sample.jpg')


INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
# branch databrowse
    'django.contrib.databrowse',
# END branch databrowse
    )

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)

