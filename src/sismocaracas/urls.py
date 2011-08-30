from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import sismocaracas.inspections as inspections
import sismocaracas.bridges as bridges
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sismocaracas.views.home', name='home'),
    # url(r'^sismocaracas/', include('sismocaracas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^inspecciones/', include(inspections.admin.admin_site.urls)),
	url(r'^puentes/', include(bridges.admin.admin_site.urls)),
)
