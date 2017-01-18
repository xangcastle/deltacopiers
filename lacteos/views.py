from django.shortcuts import render_to_response
from django.template import RequestContext
from models import recoleccion, detalle, linea, periodo
from moneycash.utils import render_to_pdf
from django_pdfkit import PDFView


def imprimir_recoleccion(request, id_recoleccion):
    rec = recoleccion.objects.get(id=id_recoleccion)
    rec.actualizar_precio()
    pagos = detalle.objects.filter(recoleccion=rec)
    ctx = {'pagos':pagos}
    return render_to_pdf('lacteos/pagos.html', ctx, "/static/lacteos/css/bootstrap.min.css")

class imprimir_recoleccion1(PDFView):
    template_name = "lacteos/pagos.html"


def imprimir_retencion(request,id_recoleccion):
    rec = recoleccion.objects.get(id=id_recoleccion)
    #rec.actualizar_precio()
    retenciones = detalle.objects.filter(recoleccion=rec)
    ctx = {'retenciones':retenciones}
    return render_to_response('print/retencion.html',ctx,context_instance=RequestContext(request))

def lista_productores(request,id_linea):
    li = linea.objects.get(id=id_linea)
    ctx = {'productores':li.productores,'linea':li}
    return render_to_response('lacteos/ListaProductores.html',ctx,context_instance=RequestContext(request))

def detalle_linea(request,id_recoleccion):
    rec = recoleccion.objects.get(id=id_recoleccion)
    rec.actualizar_precio()
    ctx = {'productores':rec.detalles,'linea':rec.linea}
    return render_to_response('lacteos/detalle_linea.html',ctx,context_instance=RequestContext(request))

def resumen_recoleccion(request,id_periodo):
    pr = periodo.objects.get(id=id_periodo)
    ctx = {'periodo':pr}
    return render_to_response('lacteos/resumen_recoleccion.html',ctx,context_instance=RequestContext(request))

def resumen_pago(request,id_periodo):
    pr = periodo.objects.get(id=id_periodo)
    ctx = {'periodo':pr}
    return render_to_response('lacteos/resumen_pago.html',ctx,context_instance=RequestContext(request))
