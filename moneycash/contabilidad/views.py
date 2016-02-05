from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import *


def imprimir_comprobante(request, id):
    comprobante = Comprobante.objects.get(id=id)
    ctx = {'comprobante': comprobante}
    return render_to_response('moneycash/contabilidad/comprobante.html',
        ctx, context_instance=RequestContext(request))
