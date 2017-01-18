from django.views.generic.base import TemplateView
from base.views import autocomplete_entidad, entidad_to_json
from .models import *
from django.http.response import HttpResponse
import json
from bson import json_util
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate
from wsgiref.util import FileWrapper
import os
from datetime import datetime
from .utils import *
from django.template.loader import render_to_string


def download_file(path):
    if not os.path.exists(path):
        return HttpResponse('Sorry. This file is not available.')
    else:
        response = HttpResponse(FileWrapper(file(path)),
            content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % \
        os.path.basename(path)
        return response


def descarga_app(request):
    path = "/var/www/deltacopiers/app.apk"
    return download_file(path)


def descarga_cendis(request):
    path = "/var/www/deltacopiers/banpro.apk"
    return download_file(path)


class index(TemplateView):
    template_name = "moneycash/base.html"
    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['tc'] = cordobizar()
        context['ventas'] = ventas()
        context['impuestos'] = impuestos()
        context['ingresos'] = ingresos_categoria()
        context['gastos'] = egresos_categoria()
        return context


class factura_venta(TemplateView):
    template_name = "moneycash/factura.html"
    def get_context_data(self, **kwargs):
        context = super(factura_venta, self).get_context_data(**kwargs)
        context['tipo_cliente'] = 'cliente'
        context['tipo_producto'] = 'vender'
        context['tc'] = cordobizar()
        return context

class facturas_venta(TemplateView):
    template_name = "moneycash/facturas.html"
    def get_context_data(self, **kwargs):
        context = super(facturas_venta, self).get_context_data(**kwargs)
        return context


class factura_compra(TemplateView):
    template_name = "moneycash/factura_compra.html"
    def get_context_data(self, **kwargs):
        context = super(factura_compra, self).get_context_data(**kwargs)
        context['tipo_cliente'] = 'proveedor'
        context['tipo_producto'] = 'comprar'
        context['tc'] = cordobizar()
        return context


class devolucion(TemplateView):
    template_name = "moneycash/devolucion.html"
    def get_context_data(self, **kwargs):
        context = super(devolucion, self).get_context_data(**kwargs)
        context['tc'] = cordobizar()
        return context


class roc(TemplateView):
    template_name = "moneycash/roc.html"

    def get_context_data(self, **kwargs):
        context = super(roc, self).get_context_data(**kwargs)
        context['bancos'] = Banco.objects.all()
        context['cuentas'] = CuentaBanco.objects.all()
        context['caja'] = True
        context['tc'] = cordobizar()
        context['tipo_cliente'] = 'cliente'
        return context


class cierre_caja(TemplateView):
    template_name = "moneycash/cierre_caja.html"

    def get_context_data(self, **kwargs):
        context = super(cierre_caja, self).get_context_data(**kwargs)
        context['caja'] = True
        context['tc'] = cordobizar()
        context['facturas'] = Factura.objects.filter(cerrada=False)
        return context


class depositos(TemplateView):
    template_name = "moneycash/depositos.html"


class facturas_no_impresas(TemplateView):
    template_name = "moneycash/facturas_no_impresas.html"

    def get_context_data(self, **kwargs):
        context = super(facturas_no_impresas, self).get_context_data(**kwargs)
        context['facturas'] = Factura.objects.filter(impresa=False, tipo="venta")
        context['tc'] = cordobizar()
        return context


class bodega(TemplateView):
    template_name = "moneycash/bodega.html"


@csrf_exempt
def tableFactura(request):
    obj = Factura
    try:
        objs = obj.objects.filter(cerrada=False, tipo="venta", impresa=True)
    except:
        pass
    table = {"data": []}
    for o in objs:
        table['data'].append(o.to_datatable())
    data = json.dumps(table, default=json_util.default)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def anular_factura(request):
    data = []
    obj_json = {}
    id_factura = request.POST.get('id_factura')
    if not id_factura:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Factura invalida"
    else:
        try:
            factura = Factura.objects.get(id=id_factura)
        except:
            factura = None

        if not factura:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Factura no encontrada"
        else:
            factura.anulada = True
            factura.save()
            obj_json['code'] = 200
            obj_json['mensaje'] = "Factura anulada!"
    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def autocomplete_cliente(request):
    return autocomplete_entidad(Cliente(), request, [('tipo', request.GET.get('tipo_cliente', '')), ])

@csrf_exempt
def autocomplete_producto(request):
    return autocomplete_entidad(Producto(), request, [(request.GET.get('tipo_producto', ''), True), ])

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
    if request.POST.get('tipo', None):
        f.tipo = request.POST.get('tipo', None)
    try:
        f.user = request.user
    except:
        f.user = User.objects.get(id=int(request.POST.get('user_id', '')))
    f.date = datetime.now()
    f.moneda = request.POST.get('monedas', '')
    if request.POST.get('factura_numero', None):
        f.numero = request.POST.get('factura_numero', '')
    else:
        f.numero = f.get_numero()
    f.cliente = extract_cliente(request)
    if request.POST.get('aplica_ir', '') == "True":
        f.aplica_ir = True
        f.ir = request.POST.get('ir', '')
        try:
            f.numero_ir = request.POST.get('numero_ir', None)
        except Exception as e:
            pass
    if request.POST.get('aplica_al', '') == "True":
        f.aplica_al = True
        f.al = request.POST.get('al', '')
        try:
            f.numero_al = request.POST.get('numero_al', None)
        except Exception as e:
            pass
    if request.POST.get('factura_tipopago', None):
        f.tipopago = request.POST.get('factura_tipopago', None)
    f.excento_iva = request.POST.get('excento_iva', '')
    f.subtotal = request.POST.get('factura_subtotal', '')
    f.descuento = request.POST.get('factura_discount', '')
    f.iva = request.POST.get('factura_iva', '')
    f.retension = request.POST.get('factura_retencion', '')
    f.total = request.POST.get('factura_total', '')
    f.saldo = request.POST.get('factura_total', '')
    f.save()
    return f


def grabar_detalle(request, factura):
    t = len(request.POST.getlist('producto_id', ''))
    data = []
    for i in range(0, t):
        dd = Detalle()
        p = Producto.objects.get(id=int(
            request.POST.getlist('producto_id', '')[i]))
        id_bodega = request.POST.getlist('bodega_id', None)[i]
        if id_bodega:
            b = Bodega.objects.get(id=int(id_bodega))
        else:
            b = None
        dd.factura = factura
        dd.producto = p
        dd.bodega = b
        dd.cantidad = float(request.POST.getlist('producto_cantidad', '')[i])
        dd.price = float(request.POST.getlist('producto_price', '')[i])
        dd.discount = float(request.POST.getlist('producto_discount', '')[i])
        dd.cost = p.cost
        dd.save()
        if b and p.almacenar:
            e, created = Existencia.objects.get_or_create(producto=p, bodega=b)
            if factura.tipo == "venta":
                e.cantidad -= dd.cantidad
            if factura.tipo == "compra":
                e.cantidad += dd.cantidad
                #p.cost = ()
            e.save()
        data.append(dd)
    return data


@csrf_exempt
def grabar_factura(request):
    data = []
    f = grabar_cabecera(request)
    grabar_detalle(request, f)
    data.append(model_to_dict(f))
    data = json.dumps(data, default=json_util.default)
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
    o = json.loads(request.POST.get('preventa', ''))
    f = Preventa()
    f.cliente = Cliente.objects.get(id=int(o['id_cliente']))
    f.save()
    for i in o['productos']:
        d = Orden()
        d.producto = Producto.objects.get(id=int(i['cod_producto']))
        d.cantidad = i['cantidad']
        d.preventa = f
        d.save()
    data = json.dumps({'preventa': f.id})
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def modelos_soportados(request):
    modelos = Modelo.objects.all()
    data = []
    for m in modelos:
        data.append(m.to_json())
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")

def generar_ecuenta(request):
    cliente = Cliente.objects.get(id=int(request.GET.get('id_cliente', '')))
    return render_to_pdf(
                'moneycash/pdf/ecuenta.html',
                {
                    'pagesize': 'LTR',
                    'cliente': cliente,
                    'documentos': cliente.ecuenta(),
                }
            )

def generar_facturas_pendientes(request):
    cliente = Cliente.objects.get(id=int(request.GET.get('id_cliente', '')))
    return render_to_pdf(
                'moneycash/pdf/facturas_pendientes.html',
                {
                    'pagesize': 'LTR',
                    'cliente': cliente,
                    'documentos': cliente.facturas(),
                }
            )

@csrf_exempt
def imprimir_factura(request):
    factura = Factura.objects.get(id=int(request.POST.get('id', '')))
    factura.impresa = True
    factura.tipopago = request.POST.get('tipopago', '')
    if request.POST.get('tipopago', '') == "contado":
        factura.saldo = 0.0
    factura.save()
    if request.POST.get('moneda', '') == "cordobas":
        factura.pasar_a_cordobas()
    elif request.POST.get('moneda', '') == "dolares":
        factura.pasar_a_dolares()
    html = render_to_string('moneycash/print/factura.html', {'f': factura})
    return HttpResponse(html)


def crear_recibo(request):
    r = Roc()
    r.cliente = Cliente.objects.get(id=int(request.POST.get('cliente_id', '')))
    r.monto = request.POST.get('pago_total', '')
    r.concepto = request.POST.get('concepto', '')
    r.moneda = request.POST.get('monedas', '')
    r.save()
    return r

def grabar_abonos(request, recibo):
    t = len(request.POST.getlist('factura', ''))
    data = []
    for i in range(0, t):
        f = Factura.objects.get(id=int(request.POST.getlist('factura', '')[i]))
        ab = Abono()
        ab.roc = recibo
        saldo = float(request.POST.getlist('saldo')[i])
        f.abonar(recibo, float(request.POST.getlist('monto')[i]), recibo.moneda,
            "Abono a Factura # " + str(f.numero) + ', quedando saldo ' + str(saldo), saldo)
        if request.POST.getlist('val_ir')[i] == "True":
            f.numero_ir = request.POST.getlist('ir')[i]
            f.aplicar_ir(recibo, request.POST.getlist('ir')[i], saldo)
        if request.POST.getlist('val_al')[i] == "True":
            f.numero_al = request.POST.getlist('al')[i]
            f.aplicar_al(recibo, request.POST.getlist('al')[i], saldo)
        data.append(ab)
    return data

@csrf_exempt
def grabar_recibo(request):
    r = crear_recibo(request)
    grabar_abonos(request, r)
    html = render_to_string('moneycash/print/recibo.html', {'r': r})
    return HttpResponse(html)


def xls_ventas_cliente(request):
    data, images = ventas_cliente()
    return render_to_excel("Ventas por Cliente", data, images)

def xls_ventas_categoria(request):
    data = [('Categoria', 'Total'), ]
    for c in ingresos_categoria():
        data.append((c['name'], c['total']))
    return render_to_excel("Ventas por Categoria", data, None)

def xls_catalogo_productos(request):
    data, images = catalogo_productos()
    return render_to_excel("Catalogo de Productos", data, images)
