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

    fields = model._meta._fields()

    writer.writerow([
            field.verbose_name.encode('utf-8')
            for field in fields])

    for element in model.objects.all():
        writer.writerow([
                unicode(getattr(element, field.name)).encode('utf-8')
                for field in fields])

    return response
