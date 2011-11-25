# -*- coding: utf-8 -*-
# Create your views here.

import csv
from django.http import HttpResponse
from .models import Building, Bridge
from .forms import InspectionGalleryForm
from django.shortcuts import render_to_response

model_url_dict = {
    'edificaciones': Building,
    'puentes':Bridge}

def csv_view(request, models_url='edificaciones'):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = \
        'attachment; filename=inspecciones_{0}.csv'.format(models_url)

    writer = csv.writer(response)

    model = model_url_dict[models_url]

    fields = model._meta._fields()

    writer.writerow([
            field.verbose_name.encode('utf-8')
            for field in fields])

    for element in model.objects.all():
        writer.writerow([
                unicode(getattr(element, field.name)).encode('utf-8')
                for field in fields])

    return response

def inspection_gallery_add(request):
    if request.method == 'POST':
        form = InspectionGalleryForm(request.POST)
    else:
        form = InspectionGalleryForm()
    return render_to_response('inspection_gallery.html', {'form': form})

