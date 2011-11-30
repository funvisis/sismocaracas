from django import forms
from .widgets import ImageWidget

class InspectionGalleryForm(forms.Form):
	
    zipe_file  = forms.FileField()
    image_widget = ImageWidget()

    def show_form(request) :
        resuts = search(request)
        if len(results) == 0 :
            pass
        else :
            pass

    def search(request):
        result = []
        return result
        #query = request.GET.get('q', '')
        
    def save(self) :
        pass

