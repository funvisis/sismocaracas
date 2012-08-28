# -*- coding: utf-8 -*-
# Django settings for sismocaracas project.

"""
La configuración de un proyecto Django en Fvis esta dividida en tres
archivos inicialmente, sin que esto limite al autor a utilizar otro
esquema de organización de la configuración.

Los tres archivos iniciales son:

* settings_base.py
* settings_dev.py
* settings_prod.py

En un momento determinado, se usa o settings_dev.py (*dev*) o
settings_prod.py (*prod*), y nunca settings_base.py (*base*). La idea
es que *dev* y *prod* importan todo lo que está en *base*.

Para evitar problemas en cuanto a encontrar una configuración
determinada, evitaremos la sobreescritura de variables de base siempre
que se pueda. Es decir, si la intención es tener un valor para una
variable en *prod* y otro en *dev*, es mejor colocar esos valores
explícitamente en *prod* y *dev* respectivamente y quitar la
declaración de esa variable de *base*. Como se tratan de archivos de
configuración, no queremos que un administrador de sistemas se confíe
al ver un valor en *base* para una variable y resulte que en *prod* la
cambiaron. Sería deseable que al momento de desplegar el proyecto, se
cree un solo archivo settings.py con el contenido de *base* y *prod*
fusionados (TODO), y así, la administración del proyecto se haga en un
solo archivo.
"""

import os
import sys
import logging

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Caracas'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ve'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z312-pfn54&ae9erx(#q0ii206fn3m89pdcl+e)hq#c0&nsarb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'sismocaracas.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sismocaracas.structuralinspections',
    'funvisis.users',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

# AUTH_PROFILE_MODULE = 'sismocaracas.inspections.Participant'
# Documentar si esto es por fvisauth
