from django.http.response import HttpResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt


def calculo_flete(peso, pais):
    decimales = peso % 0.5
    peso = peso - decimales
    if decimales > 0:
        peso = peso + 0.5
    flete = Tarifa.objects.get(zona=pais.zona, peso=peso).precio
    return flete


@csrf_exempt
def calcular_flete(request):
    pais = Pais.objects.get(id=request.POST.get('pais', ''))
    peso = float(request.POST.get('peso', ''))
    flete = 0.0
    if peso <= 20:
        flete = calculo_flete(peso, pais)
    elif peso > 20 < 30:
        flete = 459.71 + (peso - 20) * 0.5 * 8.22
    elif peso > 30 < 70:
        flete = 624.16 + (peso - 30) * 19.86
    elif peso > 70 < 300:
        flete = 1418.46 + (peso - 70) * 23.89
    else:
        flete = 6912.59 + (peso - 300) * 23.89
    data = json.dumps({'flete': flete, 'Ext._Responsabilidad': flete * 0.03,
    'Fuel_Surcharge': flete * 0.02, 'total': round(flete * 1.05, 2)})
    return HttpResponse(data, content_type="application/json")
