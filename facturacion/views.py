from django.http.response import HttpResponse
import json
from .models import *


def autocomplete_cliente(request):
    if request.is_ajax:
        result = []

        qs = Cliente.objects.filter(
            Q(identificacion__istartswith=request.GET.get('term', '')) |
            Q(name__icontains=request.GET.get('term', ''))
            )
        for obj in qs:
            obj_json = {}
            obj_json['label'] = str(obj)
            obj_json['value'] = str(obj.name)
            obj_json['obj'] = model_to_dict(obj)
            result.append(obj_json)

        data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')