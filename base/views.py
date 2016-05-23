from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.db.models import Q
import json


def autocomplete_entidad(instance, request):
    if request.is_ajax:
        model = type(instance)
        result = []
        term = request.GET.get('term', None)
        code = request.GET.get('code', None)
        if term:
            qs = model.objects.filter(
                Q(code__istartswith=term) |
                Q(name__icontains=term)
                )
            for obj in qs:
                obj_json = {}
                obj_json['label'] = obj.name
                obj_json['value'] = obj.name
                obj_json['obj'] = model_to_dict(obj)
                result.append(obj_json)
        if code:
            obj = model.objects.get(code=code)
            obj_json = {}
            obj_json['label'] = obj.name
            obj_json['value'] = obj.name
            obj_json['obj'] = model_to_dict(obj)
            result.append(obj_json)
        data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')


def entidad_to_json(instance, request):
    if request.is_ajax:
        model = type(instance)
        result = []
        id = request.POST.get('id', None)
        obj = model.objects.get(id=id)
        if obj:
            try:
                result = obj.to_json()
            except:
                result = model_to_dict(obj)
            data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')
