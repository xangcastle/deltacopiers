from django.views.generic.base import TemplateView
from base.views import autocomplete_entidad, entidad_to_json
from .models import *
from django.http.response import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate


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
        context['tipo_pagos'] = TipoPago.objects.all().order_by('name')
        return context


class bodega(TemplateView):
    template_name = "moneycash/bodega.html"

@csrf_exempt
def autocomplete_cliente(request):
    return autocomplete_entidad(Cliente(), request)

@csrf_exempt
def autocomplete_producto(request):
    return autocomplete_entidad(Producto(), request)

@csrf_exempt
def detalle_producto(request):
    return entidad_to_json(Producto(), request)

@csrf_exempt
def detalle_cliente(request):
    return entidad_to_json(Cliente(), request)


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
    try:
        f.user = request.user
    except:
        f.user = User.objects.get(id=int(request.POST.get('user_id', '')))
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
    f.tipopago = request.POST.get('factura_tipopago', '')
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


@csrf_exempt
def grabar_factura(request):
    data = []
    f = grabar_cabecera(request)
    grabar_detalle(request, f)
    data.append(model_to_dict(f))
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def clientes(request):
    queryset = Cliente.objects.all()
    if queryset:
        data = serializers.serialize('json', queryset)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def grud_cliente(request):
    obj_json = {}
    obj_json['id'] = request.POST.get('id', None)
    obj_json['code'] = request.POST.get('code', '')
    obj_json['name'] = request.POST.get('name', '')
    obj_json['ident'] = request.POST.get('ident', '')
    obj_json['phone'] = str(request.POST.get('phone', ''))
    obj_json['email'] = request.POST.get('email', '')
    obj_json['address'] = request.POST.get('address', '')
    if obj_json['id']:
        try:
            c = Cliente.objects.get(id=obj_json['id'])
            c.code = obj_json['code']
            c.name = obj_json['name']
            c.ident = obj_json['ident']
            c.phone = obj_json['phone']
            c.email = obj_json['email']
            c.address = obj_json['address']
            c.save()
            obj_json['message'] = "Cliente actualizado con exito"
        except:
            obj_json['message'] = "Cliente no encontrado"
    elif len(obj_json['name']) > 0:
        c = Cliente()
        c.code = obj_json['code']
        c.name = obj_json['name']
        c.ident = obj_json['ident']
        c.phone = obj_json['phone']
        c.email = obj_json['email']
        c.address = obj_json['address']
        c.save()
        obj_json['message'] = "Cliente agregado con exito"
    else:
        obj_json['message'] = "No hay datos Validos"
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def movil_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        data = serializers.serialize('json', [user, ])
        struct = json.loads(data)
        data = json.dumps(struct[0])
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def movil_facturas(request):
    user = User.objects.get(id=int(request.POST.get('id', '')))
    queryset = Factura.objects.filter(user=user)
    if queryset:
        data = serializers.serialize('json', queryset)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def tipos_pago(request):
    tp = TipoPago.objects.all()
    data = []
    if tp:
        data = serializers.serialize('json', tp)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def catalogo(request):
    inventory = []
    for p in Producto.objects.all():
        if p.imagen:
            inventory.append(p)
    data = []
    if inventory:
        data = serializers.serialize('json', inventory)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = []
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_sms(request):
    code = request.POST.get('codigo', None)
    numero = request.POST.get('numero', None)
    nombre = request.POST.get('nombre', None)
    if code and numero and nombre:
        send_sms("Estimado/a %s, es un placer darte la bienvenida. Tu codigo de registro es %s"
        % (nombre, code), numero)
        user, created = Cliente.objects.get_or_create(name=nombre, phone=numero)
        user.save()
        data = json.dumps([user.to_json(), ])
    else:
        data = json.dumps([{'error': "por favor envia las variables codigo, numero y nombre."}, ])
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def mensajes_pendientes(request):
    mensajes = SMS.objects.filter(enviado=False)
    data = []
    for m in mensajes:
        data.append(m.to_json())
    data = json.dumps(data)
    mensajes.update(enviado=True)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def preventa(request):
    o = request.POST.get('preventa', '')
    f = Preventa()
    f.cliente = Cliente.objects.get(id=o['id_cliente'])
    f.save()
    for d in o['productos']:
        d = Orden()
        d.producto = d['cod_producto']
        d.cantidad = d['cantidad']
        d.preventa = f
        d.save()
    data = json.dumps([{'preventa': f.id}, ])
    return HttpResponse(data, content_type="application/json")
