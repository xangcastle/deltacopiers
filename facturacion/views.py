from django.http.response import HttpResponse
import json
from .models import *
from django.db.models import Q
from django.forms.models import model_to_dict

def autocomplete_cliente(request):
    if request.is_ajax:
        result = []
        qs = Cliente.objects.filter(
                Q(identificacion__istartswith=request.GET.get('term', '')) |
                Q(name__icontains=request.GET.get('term', ''))
            )
        if qs.count() > 0:
            for obj in qs:
                obj_json = {}
                obj_json['label'] = str(obj)
                obj_json['value'] = str(obj[request.GET.get('opt')])
                obj_json['obj'] = model_to_dict(obj)
                result.append(obj_json)
        data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')

def autocomplete_producto(request):
    if request.is_ajax:
        result = []
        obj = Producto.objects.get(code = request.GET.get('term', ''));
        if obj.count() > 0:
            obj_json = {}
            obj_json['label'] = str(obj)
            obj_json['value'] = str(obj.code)
            obj_json['obj'] = model_to_dict(obj)
            result.append(obj_json)
        data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')
