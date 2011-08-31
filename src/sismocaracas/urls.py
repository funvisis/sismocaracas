from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^edificaciones/', include('sismocaracas.buildings.urls')),
    url(r'^puentes/', include('sismocaracas.bridges.urls'))
    )
