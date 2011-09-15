# -*- coding: utf-8 -*-

"""
This package define all the admin sites used by the application.

The package collects modules associated to models, and every module
define a ModelAdmin for every site where is needed.

By now, every ModelAdmin from every module inside this package is
imported by hand and registered when needed.

Maybe it could be possible automate these proccess by defining a
tupple in every module with una Model and one ModelAdmin or with one
Model, and iterate over every module inside this package and register
those tuples.

To associate a tuple with an specific admin site, a dict  could be
used instead of only the tuple (i.e a dict of sites:tuples)

The only issue to resolve when automated is the authorization
issue. How to associate an admin_site with an authorization
evaluation...
"""

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from ..models import Building
from ..models import Bridge

from .building import BuildingAdmin
from .bridge import BridgeAdmin

admin_site = AdminSite('admin_site')

admin_site.register(Building, BuildingAdmin)
admin_site.register(Bridge, BridgeAdmin)

