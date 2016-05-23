from django.views.generic.base import TemplateView
from base.views import autocomplete_entidad, entidad_to_json
from .models import *
from django.http.response import HttpResponse
from django.template import RequestContext
import json


class index(TemplateView):
    template_name = "moneycash/base.html"


class factura(TemplateView):
    template_name = "moneycash/factura.html"
    def get_context_data(self, **kwargs):
        context = super(factura, self).get_context_data(**kwargs)
        context['tipo_pagos'] = TipoPago.objects.all()
        return context


class roc(TemplateView):
    template_name = "moneycash/roc.html"


class facturas_no_impresas(TemplateView):
    template_name = "moneycash/facturas_no_impresas.html"
    def get_context_data(self, **kwargs):
        context = super(facturas_no_impresas, self).get_context_data(**kwargs)
        context['facturas'] = Factura.objects.filter(impresa=False)
        return context


class bodega(TemplateView):
    template_name = "moneycash/bodega.html"


def autocomplete_cliente(request):
    return autocomplete_entidad(Cliente(), request)


def autocomplete_producto(request):
    return autocomplete_entidad(Producto(), request)


def detalle_producto(request):
    return entidad_to_json(Producto(), request)
    

def detalle_factura(request):
    return entidad_to_json(Factura(), request)


def extract_cliente(request):
    id = request.POST.get('cliente_id', None)
    if id:
        c = Cliente.objects.get(id=int(id))
        c.phone = request.POST.get('cliente_phone', '')
        c.email = request.POST.get('cliente_email', '')
        c.address = request.POST.get('cliente_address', '')
        c.save()
    else:
        c, created = Cliente.objects.get_or_create(
            ident=request.POST.get('cliente_ident', ''))
        c.name = request.POST.get('cliente_name', '')
        c.phone = request.POST.get('cliente_phone', '')
        c.email = request.POST.get('cliente_email', '')
        c.address = request.POST.get('cliente_address', '')
        c.save()
    return c


def grabar_cabecera(request):
    f = Factura()
    f.user = request.user
    f.numero = 1
    f.cliente = extract_cliente(request)
    f.aplica_ir = request.POST.get('aplica_ir', '')
    f.aplica_al = request.POST.get('aplica_al', '')
    f.excento_iva = request.POST.get('excento_iva', '')
    f.subtotal = request.POST.get('factura_subtotal', '')
    f.descuento = request.POST.get('factura_discount', '')
    f.iva = request.POST.get('factura_iva', '')
    f.retension = request.POST.get('factura_retencion', '')
    f.total = request.POST.get('factura_total', '')
    f.save()
    return f


def grabar_detalle(request, factura):
    t = len(request.POST.getlist('producto_id', ''))
    data = []
    for i in range(0, t):
        dd = Detalle()
        p = Producto.objects.get(id=int(
            request.POST.getlist('producto_id', '')[i]))
        b = Bodega.objects.get(id=int(
            request.POST.getlist('bodega_id', '')[i]))
        e = p.existencias().filter(bodega=b)[0]
        dd.factura = factura
        dd.producto = p
        dd.bodega = b
        dd.cantidad = float(request.POST.getlist('producto_cantidad', '')[i])
        dd.price = float(request.POST.getlist('producto_price', '')[i])
        dd.discount = float(request.POST.getlist('producto_discount', '')[i])
        dd.cost = p.cost
        dd.save()
        e.cantidad -= dd.cantidad
        e.save()
        data.append(dd)
    return data


def grabar_factura(request):
    data = []
    f = grabar_cabecera(request)
    grabar_detalle(request, f)
    data.append(model_to_dict(f))
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
