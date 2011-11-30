# -*- coding: utf-8 -*-

from ..models import InspectionGallery

from django.contrib import admin
from django import forms

from photologue.models import GalleryUpload

class InspectionGalleryForm(forms.ModelForm):

    #gallery_upload = GalleryUpload
    #tittle = forms.CharField(label='fuck you!')

    class Meta:
        model = InspectionGallery
        exclude = ['date_added', 'title', 'title_slug', 'description', 'is_public', 'tags']

class InspectionGalleryAdmin(admin.ModelAdmin):
    form = InspectionGalleryForm
    
