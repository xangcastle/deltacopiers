from django.http.response import HttpResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def calcular_flete(request):
    pais = Pais.objects.get(id=request.POST.get('pais', ''))
    peso = float(request.POST.get('peso', ''))
    decimales = peso % 0.5
    peso = peso - decimales
    if decimales > 0:
        peso = peso + 0.5
    flete = Tarifa.objects.get(zona=pais.zona, peso=peso).precio
    data = json.dumps({'flete': flete, 'Ext._Responsabilidad': flete * 0.03,
    'Fuel_Surcharge': flete * 0.02, 'total': round(flete * 1.05, 2)})
    return HttpResponse(data, content_type="application/json")
