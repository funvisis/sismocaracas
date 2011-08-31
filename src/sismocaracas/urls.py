from django.conf.urls.defaults import patterns, include, url

from django.contrib import auth
from django.contrib import admin

admin.site.register(auth.models.Group)
admin.site.register(auth.models.User)
#admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^inspecciones/', include('sismocaracas.buildings.urls')),
#    url(r'^puentes/', include('sismocaracas.bridges.urls')),
    (r'^admin/', include(admin.site.urls)),
    )
