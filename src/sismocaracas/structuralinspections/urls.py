from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from .admin import admin_site
# from .admin.revisor import  revisor_admin_site
# from .admin.inspector import  inspector_admin_site

from .views import csv_view
from .views import inspection_gallery_add

part_patterns = ['']
part_patterns.append(url(r'^csv/(?P<models_url>\w+)/', csv_view))

# branch databrowse
if any('databrowse' in app for app in settings.INSTALLED_APPS):
    from django.contrib import databrowse
    from .models import Building, Bridge
    map(databrowse.site.register, (Building, Bridge))
    part_patterns.append(url(r'^databrowse/(.*)', databrowse.site.root))
# END branch databrowse

part_patterns.append(url(r'', include(admin_site.urls)))
part_patterns.append(url(r'structuralinspections/inspectiongallery/add/', inspection_gallery_add))

urlpatterns = patterns(*part_patterns)
