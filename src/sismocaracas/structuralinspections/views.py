# -*- coding: utf-8 -*-
# Create your views here.

import csv
from django.http import HttpResponse
from .models import Building, Bridge

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

    field_names = model._meta.get_all_field_names()

    writer.writerow([
            model._meta.get_field(field_name).verbose_name.encode('utf-8')
            for field_name in field_names])

    for element in model.objects.all():
        writer.writerow([
                unicode(getattr(element, field_name)).encode('utf-8')
                for field_name in field_names])

    return response
