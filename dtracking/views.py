from django.http.response import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth import authenticate
from geoposition import Geoposition


@csrf_exempt
def movil_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        o = {'username': user.username, 'name': user.get_full_name()}
        try:
            profile = Gestor.objects.get(user=user)
            o['perfil'] = profile.to_json()
        except:
            o['error'] = "el usuario no tiene perfil o esta inactivo."
        data = json.dumps([o])
    else:
        data = []
    return HttpResponse(data, content_type='application/json')


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


@csrf_exempt
def cargar_gestion(request):
    g = Gestion.objects.filter(id=int(request.POST.get('gestion', '')))
    g.fecha = request.POST.get('fecha', '')
    g.position = Geoposition(request.POST.get('latitude', ''),
    request.POST.get('longitude', ''))
    g.json = request.POST.get('json', '')
    g.save()
    data = [g, ]
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
