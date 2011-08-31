from django.conf.urls.defaults import patterns, include, url
from .admin import admin_site

urlpatterns = patterns(
    '',
    url(r'^$', include(admin_site.urls)),
    )
