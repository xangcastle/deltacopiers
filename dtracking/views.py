from django.http.response import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core import serializers


@csrf_exempt
def tipos_gestion(request):
    tg = TipoGestion.objects.all()
    data = []
    for t in tg:
        data.append(t.to_json())
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def gestiones_pendientes(request):
    gs = Gestion.objects.filter(user=int(request.POST.get('user', '')),
    realizada=False)
    data = []
    for g in gs:
        data.append(g.to_json())
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
