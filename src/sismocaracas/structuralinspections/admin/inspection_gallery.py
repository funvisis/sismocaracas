# -*- coding: utf-8 -*-

from ..models import InspectionGallery

from django.contrib import admin
from django import forms

from photologue.models import GalleryUpload

class InspectionGalleryForm(forms.ModelForm):

    class Meta:
        model = InspectionGallery
        exclude = ['date_added']

class InspectionGalleryAdmin(admin.ModelAdmin):
    form = InspectionGalleryForm
    
