from django import forms
from .widgets import AdminImageWidget

class InspectionGalleryForm(forms.Form):
    gallery_name = forms.CharField()
    zipe_file  = forms.FileField()
    image = forms.FileField(widget=AdminImageWidget)

