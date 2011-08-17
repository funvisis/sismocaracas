import os
import sys

path = os.getcwd().rsplit('/', 1)[0]
sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sismocaracas.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
