from django.conf.urls.defaults import patterns, include, url

import sismocaracas.buildings.admin
import sismocaracas.bridges.admin
 
urlpatterns = patterns(
    '',
    url(r'^edificaciones/', include(sismocaracas.buildings.admin.admin_site.urls)),
    url(r'^puentes/', include(sismocaracas.bridges.admin.admin_site.urls))
    )
