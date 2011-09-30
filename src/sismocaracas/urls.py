from django.conf.urls.defaults import patterns, include, url

from django.contrib import auth
from django.contrib import admin

from funvisis.django.fvisusers.models import FVISUser


admin.site.register(FVISUser)
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^inspecciones/', include('sismocaracas.structuralinspections.urls')),
    (r'^admin/', include(admin.site.urls)),
    )
