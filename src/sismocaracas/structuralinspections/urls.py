from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from .admin import admin_site
from .views import csv_view

part_patterns = ['']
part_patterns.append(url(r'^csv/(?P<models_url>\w+)/', csv_view))

part_patterns.append(url(r'', include(admin_site.urls)))

urlpatterns = patterns(*part_patterns)
