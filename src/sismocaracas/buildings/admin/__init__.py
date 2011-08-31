# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from ..models import Building
#from ..models import Bridge
from .supervisor import BuildingAdmin

admin_site = AdminSite('admin_site')

admin_site.register(Building, BuildingAdmin)
#admin_sire.register(Brige)
