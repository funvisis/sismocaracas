from django.conf.urls.defaults import patterns, include, url
from .admin import admin_site
# from .admin.revisor import  revisor_admin_site
# from .admin.inspector import  inspector_admin_site

from .views import csv_view

urlpatterns = patterns(
    '',
    url(r'^csv/(?P<models_url>\w+)/', csv_view),
    url(r'', include(admin_site.urls)),
    )
