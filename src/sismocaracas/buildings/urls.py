from django.conf.urls.defaults import patterns, include, url
from .admin.supervisor import admin_site as supervisor_admin_site
# from .admin.revisor import admin_site as revisor_admin_site
# from .admin.inspector import admin_site as inspector_admin_site

urlpatterns = patterns(
    '',
    url(r'^supervisor/', include(supervisor_admin_site.urls)),
    )
