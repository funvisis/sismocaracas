from django.conf.urls.defaults import patterns, include, url
from .admin import admin_site
# from .admin.revisor import  revisor_admin_site
# from .admin.inspector import  inspector_admin_site

urlpatterns = patterns(
    '',
    url(r'', include(admin_site.urls)),
    )
