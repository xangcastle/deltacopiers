from __future__ import unicode_literals

from django.db import models
from base.models import Entidad
from django.forms.models import model_to_dict
#from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum, Max, F
from datetime import datetime, timedelta

#User = settings.AUTH_USER_MODEL


MONEDAS = (("cordobas", "C$ Cordobas"), ("dolares", "U$ Dolares"))

class TC(models.Model):
    fecha = models.DateField()
    oficial = models.FloatField()
    venta = models.FloatField(null=True)
    compra = models.FloatField(null=True)

def dolarizar(cordobas=1, fecha=datetime.now(), digitos=2):
    tc = TC.objects.get(fecha__year=fecha.year, fecha__month=fecha.month,
        fecha__day=fecha.day)
    if tc.venta and tc.venta > tc.oficial:
        tc = tc.venta
    else:
        tc = tc.oficial
    return round(cordobas / tc, digitos)

def cordobizar(dolares=1, fecha=datetime.now(), digitos=2):
    tc = TC.objects.get(fecha__year=fecha.year, fecha__month=fecha.month,
        fecha__day=fecha.day)
    if tc.compra and tc.compra < tc.oficial:
        tc = tc.compra
    else:
        tc = tc.oficial
    return round(dolares * tc, digitos)

class Banco(Entidad):
    pass

class CuentaBanco(models.Model):
    banco = models.ForeignKey(Banco)
    numero = models.CharField(max_length=30)
    moneda = models.CharField(max_length=25, default="cordobas", choices=MONEDAS)

    def __unicode__(self):
        return "%s %s- %s" % (self.banco.name, self.moneda, self.numero)

class Sucursal(Entidad):
    pass

class Bodega(Entidad):
    sucursal = models.ForeignKey(Sucursal)

class datos_generales(models.Model):
    ident = models.CharField(max_length=14, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=125, null=True, blank=True)
    address = models.TextField(max_length=400, null=True, blank=True)

    class Meta:
        abstract = True

TIPOS_CLIENTE = (
('cliente', "CLIENTE"),
('proveedor', "PROVEEDOR"),
)


class Cliente(datos_generales, Entidad):
    tipo = models.CharField(max_length=20, default="cliente", choices=TIPOS_CLIENTE)
    limite_credito = models.FloatField(default=0.0)
    cuenta_credito = models.ForeignKey('cuenta_credito', null=True, blank=True)

    def facturas(self):
        return Factura.objects.filter(cliente=self, impresa=True, saldo__gt=0.0)

    def saldo(self):
        data = {}
        cordobas =  self.facturas().filter(moneda="cordobas")
        dolares =  self.facturas().filter(moneda="dolares")
        if cordobas.count() > 0:
            data['cordobas'] = cordobas.aggregate(Sum('saldo'))['saldo__sum']
        else:
            data['cordobas'] = 0.0
        if dolares.count() > 0:
            data['dolares'] = dolares.aggregate(Sum('saldo'))['saldo__sum']
        else:
            data['dolares'] = 0.0
        data['total_cordobas'] = cordobizar(data['dolares']) + data['cordobas']
        data['total_dolares'] = dolarizar(data['cordobas']) + data['dolares']
        return data

    def saldo_disponible(self):
        return self.limite_credito - (self.saldo()['cordobas'] + cordobizar(self.saldo()['dolares']))

    def ecuenta(self):
        data = []
        facturas = Factura.objects.filter(cliente=self, impresa=True)
        for f in facturas:
            if f.moneda == "cordobas":
                data.append({'fecha': f.date,
                'referencia': "F - " + str(f.numero),
                'descripcion': "Factura Numero " + str(f.numero),
                'cordobas': f.total,
                'dolares': 0.0})
                if f.aplica_ir:
                    print("aplica ir")
                    data.append({'fecha': f.date,
                    'referencia': "IR - " + str(f.numero_ir),
                    'descripcion': "Retencion en la Fuente # " + str(f.numero_ir),
                    'cordobas': -f.ir,
                    'dolares': 0.0})
                if f.aplica_al:
                    data.append({'fecha': f.date,
                    'referencia': "AL - " + str(f.numero_al),
                    'descripcion': "Retencion Alcaldia Municipal # " + str(f.numero_al),
                    'cordobas': -f.al,
                    'dolares': 0.0})
            else:
                data.append({'fecha': f.date,
                'referencia': "F - " + str(f.numero),
                'descripcion': "Factura Numero " + str(f.numero),
                'dolares': f.total,
                'cordobas': 0.0})
                if f.aplica_ir:
                    print("aplica ir")
                    data.append({'fecha': f.date,
                    'referencia': "IR - " + str(f.numero_ir),
                    'descripcion': "Retencion en la Fuente # " + str(f.numero_ir),
                    'dolares': -f.ir,
                    'cordobas': 0.0})
                if f.aplica_al:
                    data.append({'fecha': f.date,
                    'referencia': "AL - " + str(f.numero_al),
                    'descripcion': "Retencion Alcaldia Municipal # " + str(f.numero_al),
                    'dolares': -f.al,
                    'cordobas': 0.0})
        abonos = Roc.objects.filter(cliente=self)
        for a in abonos:
            if a.moneda == "cordobas":
                data.append({'fecha': a.fecha,
                'referencia': "ROC - " + str(a.numero),
                'descripcion': a.concepto,
                'dolares': 0.0,
                'cordobas': -a.monto})
            else:
                data.append({'fecha': a.fecha,
                'referencia': "ROC - " + str(a.numero),
                'descripcion': a.concepto,
                'cordobas': 0.0,
                'dolares': -a.monto})
        data = sorted(data, key=lambda doc: doc['fecha'], reverse=False)
        return data

    def to_json(self):
        obj = super(Cliente, self).to_json()
        obj['facturas'] = []
        for f in self.facturas():
            obj['facturas'].append(f.to_json())
        obj['saldo'] = self.saldo()
        obj['saldo_disponible'] = self.saldo_disponible()
        return obj


class Categoria(Entidad):
    parent = models.ForeignKey('self', null=True, blank=True)

class Producto(Entidad):
    categoria = models.ForeignKey(Categoria, null=True)
    short_name = models.CharField(max_length=25, null=True, blank=True)
    no_part = models.CharField(max_length=25, null=True)
    price = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True)
    details = models.TextField(max_length=255, null=True, blank=True)
    vender = models.BooleanField(default=False)
    comprar = models.BooleanField(default=False)
    almacenar = models.BooleanField(default=False)

    def existencias(self):
        return Existencia.objects.filter(producto=self)

    def existencia_enbodega(self, bodega):
        try:
            return Existencia.objects.get(producto=self, bodega=bodega).cantidad
        except:
            return 0.0

    def existencias_json(self):
        data = []
        for b in Bodega.objects.all().order_by('name'):
            data.append({'bodega': b.name, 'cantidad': self.existencia_enbodega(b), 'bodega_id': b.id})
        return data

    def url_imagen(self):
        if self.imagen:
            return self.imagen.url
        else:
            return "#"

    def salidas(self):
        return salidaDetalle.objects.filter(producto=self)

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="60" />' % (self.imagen)
    image_thumb.allow_tags = True
    image_thumb.short_description = "Imagen"

    def to_json(self):
        obj = {}
        obj['id'] = self.id
        obj['code'] = self.code
        obj['name'] = self.name
        obj['activo'] = self.activo
        obj['no_part'] = self.no_part
        obj['price'] = self.price
        obj['cost'] = self.cost
        obj['almacenar'] = self.almacenar
        obj['imagen'] = self.url_imagen()
        obj['details'] = self.details
        obj['existencias'] = self.existencias_json()
        return obj

    def existencia_total(self):
        if self.existencias():
            return self.existencias().aggregate(Sum('cantidad'))['cantidad__sum']
        else:
            return 0.0

    def con_imagen(self):
        if self.imagen:
            return True
        else:
            return False


class Existencia(models.Model):
    bodega = models.ForeignKey(Bodega)
    producto = models.ForeignKey(Producto)
    cantidad = models.FloatField(default=0.0)


TIPOS_FACTURA = (
("venta", "VENTA"),
("compra", "COMPRA"),
)

TIPOS_PAGO = (
("contado", "CONTADO"),
("credito", "CREDITO"),
)


class Factura(models.Model):
    tipo = models.CharField(max_length=20, default="venta", choices=TIPOS_FACTURA)
    sucursal = models.ForeignKey(Sucursal, null=True, blank=True)
    moneda = models.CharField(max_length=25, null=True, choices=MONEDAS)
    user = models.ForeignKey(User, null=True,
        related_name="moneycash_factura_user")
    date = models.DateTimeField()
    numero = models.PositiveIntegerField(null=True)
    cliente = models.ForeignKey(Cliente, null=True)
    subtotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)

    excento_iva = models.BooleanField(default=False)
    iva = models.FloatField(null=True)

    aplica_ir = models.BooleanField(default=False)
    ir = models.FloatField(null=True, blank=True)
    numero_ir = models.PositiveIntegerField(null=True, blank=True)

    aplica_al = models.BooleanField(default=False)
    al = models.FloatField(null=True, verbose_name="alcaldia", blank=True)
    numero_al = models.PositiveIntegerField(null=True, blank=True)

    total = models.FloatField(null=True)
    tipopago = models.CharField(max_length=25, null=True, choices=TIPOS_PAGO)
    saldo = models.FloatField(null=True)

    impresa = models.BooleanField(default=False)
    cerrada = models.BooleanField(default=False)
    entregada = models.BooleanField(default=False)
    anulada = models.BooleanField(default=False)
    dec_ir = models.BooleanField(default=False)
    dec_al = models.BooleanField(default=False)
    dec_iva = models.BooleanField(default=False)

    def __unicode__(self):
        return "Factura No " + str(self.numero)

    def simbolo(self):
        if self.moneda == "cordobas":
            return "C$"
        else:
            return "U$"

    def to_json(self):
        obj = model_to_dict(self)
        obj['date'] = str(self.date)
        obj['calculo_ir'] = self.calculo_ir()
        obj['calculo_al'] = self.calculo_al()
        obj['detalle'] = self.detalle_json()
        cliente = model_to_dict(self.cliente)
        if self.moneda == "cordobas":
            cliente['limite_credito'] = self.cliente.limite_credito
            cliente['saldo'] = self.cliente.saldo()['total_cordobas']
            cliente['saldo_disponible'] = self.cliente.saldo_disponible()
        else:
            cliente['limite_credito'] = dolarizar(self.cliente.limite_credito,
                self.date)
            cliente['saldo'] = self.cliente.saldo()['total_dolares']
            cliente['saldo_disponible'] = dolarizar(
                self.cliente.saldo_disponible())
        obj['cliente_data'] = cliente
        return obj

    def to_datatable(self):
        return {'numero': self.numero, 'cliente': self.cliente.name,
            'ruc': self.cliente.ident, 'subtotal': self.subtotal,
            'moneda': self.moneda, 'descuento': self.descuento, 'iva': self.iva,
            'total': self.total}

    def to_obj_pdfjs(self):
        obj = {'numero': str(self.numero),
            'cliente': self.cliente.name + " - " + self.cliente.ident,
            'direccion': self.cliente.address,
            'telefono': self.cliente.phone,
            'contacto': "",
            'area': "",
            'dia': str(self.date.day),
            'mes': str(self.date.month),
            'anno': str(self.date.year),
            'tc': str(cordobizar(1, self.date)),
            'fecha_vence': "",
            'subtotal': str(self.subtotal),
            'subtotal_cordobas': str(self.subtotal_cordobas()),
            'iva': str(self.iva),
            'total': str(self.total)}
        if self.tipopago == "contado":
            obj['contado'] = "X"
        else:
            obj['contado'] = ""
        if self.tipopago == "credito":
            obj['credito'] = "X"
        else:
            obj['credito'] = ""
        return obj

    def tc(self):
        return cordobizar(1, self.date, digitos=4)

    def pasar_a_dolares(self):
        if self.moneda == "cordobas":
            self.moneda = "dolares"
            for d in self.detalle():
                d.price = dolarizar(d.price, self.date)
                d.cost = dolarizar(d.cost, self.date)
                d.save()
            self.subtotal = dolarizar(self.subtotal, self.date)
            self.iva = dolarizar(self.iva, self.date)
            self.total = dolarizar(self.total, self.date)
            self.saldo = dolarizar(self.saldo, self.date)
            self.save()

    def pasar_a_cordobas(self):
        if self.moneda == "dolares":
            self.moneda = "cordobas"
            for d in self.detalle():
                d.price = cordobizar(d.price, self.date)
                d.cost = cordobizar(d.cost, self.date)
                d.save()
            self.subtotal = cordobizar(self.subtotal, self.date)
            self.iva = cordobizar(self.iva, self.date)
            self.total = cordobizar(self.total, self.date)
            self.saldo = cordobizar(self.saldo, self.date)
            self.save()

    def get_numero(self):
        try:
            return Factura.objects.all(
                ).aggregate(Max('numero'))['numero__max'] + 1
        except:
            return 1

    def calculo_ir(self):
        if self.moneda == "cordobas":
            if self.subtotal > 1000:
                return round(self.subtotal * 0.02, 2)
            else:
                return 0.0
        else:
            if cordobizar(self.subtotal) > 1000:
                return round(self.subtotal * 0.02, 2)
            else:
                return 0.0

    def calculo_al(self):
        if self.moneda == "cordobas":
            if self.subtotal > 1000:
                return round(self.subtotal * 0.01, 2)
            else:
                return 0.0
        else:
            if cordobizar(self.subtotal) > 1000:
                return round(self.subtotal * 0.01, 2)
            else:
                return 0.0

    def detalle(self):
        return Detalle.objects.filter(factura=self)

    def detalle_json(self):
        return [x.to_json() for x in self.detalle()]

    def subtotal_cordobas(self):
        if self.moneda == "cordobas":
            return self.subtotal
        else:
            return cordobizar(self.subtotal)

    def iva_cordobas(self):
        if self.moneda == "cordobas":
            return self.iva
        else:
            return cordobizar(self.iva)

    def total_cordobas(self):
        if self.moneda == "cordobas":
            return self.total
        else:
            return cordobizar(self.total, self.date)

    def subtotal_dolares(self):
        if self.moneda == "cordobas":
            return dolarizar(self.subtotal, self.date)
        else:
            return self.subtotal

    def abonar(self, recibo, monto, moneda, comentario="", saldo=0.0):
        abono = 0.0
        if self.moneda == moneda:
            abono = monto
        else:
            if self.moneda == "cordobas" and moneda == "dolares":
                abono = cordobizar(monto)
            else:
                abono = dolarizar(monto)
        self.saldo = round(self.saldo - abono, 2)
        self.save()
        ab = Abono(factura=self, monto=monto, roc=recibo,
            comentario=comentario, saldo=saldo)
        ab.save()

    def aplicar_ir(self, recibo, numero, saldo):
        abono = self.calculo_ir()
        self.abonar(recibo, abono, self.moneda, "Retencion IR # " + numero + "aplica a factura # " + str(self.numero), saldo)
        self.aplica_ir = True
        self.ir = abono
        self.save()

    def aplicar_al(self, recibo, numero, saldo):
        abono = self.calculo_al()
        self.abonar(recibo, abono, self.moneda,
            "Retencion Alcaldia Municipal # " + numero + "aplica a factura # " + str(self.numero), saldo)
        self.aplica_al = True
        self.al = abono
        self.save()


class Detalle(models.Model):
    factura = models.ForeignKey(Factura, null=True)
    producto = models.ForeignKey(Producto)
    cantidad = models.FloatField()
    price = models.FloatField()
    discount = models.FloatField(null=True)
    cost = models.FloatField()

    bodega = models.ForeignKey(Bodega, null=True, blank=True)
    existencia = models.FloatField(null=True)
    saldo = models.FloatField(null=True)
    existencia_total = models.FloatField(null=True)
    saldo_total = models.FloatField(null=True)
    costo_promedio = models.FloatField(null=True)

    def __unicode__(self):
        return self.producto.name

    def to_json(self):
        return model_to_dict(self)

    def aplicar(self):
        pass

    def total(self):
        return self.cantidad * self.price

    def precio_impreso(self):
        if self.factura.moneda == "cordobas":
            return dolarizar(self.price, self.factura.date, 3)
        else:
            return self.price

    def total_impreso(self):
        return round(self.cantidad * self.precio_impreso(), 2)


class compra_manager(models.Manager):
    def get_queryset(self):
        return super(compra_manager, self).get_queryset().filter(tipo='compra')


class Compra(Factura):
    objects = models.Manager()
    objects = compra_manager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.tipo = 'compra'
        self.moneda = 'cordobas'
        super(Compra, self).save()



class Roc(models.Model):
    numero = models.PositiveIntegerField(null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente)
    monto = models.FloatField(default=0.0)
    concepto = models.TextField(max_length=999, null=True)
    moneda = models.CharField(max_length=25, default="cordobas", choices=MONEDAS)

    def get_numero(self):
        try:
            return Roc.objects.all(
                ).aggregate(Max('numero'))['numero__max'] + 1
        except:
            return 1

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.get_numero()
        super(Roc, self).save()

class Abono(models.Model):
    roc = models.ForeignKey(Roc)
    factura = models.ForeignKey(Factura)
    monto = models.FloatField(default=0.0)
    saldo = models.FloatField(null=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)


class Efectivo(models.Model):
    roc = models.ForeignKey(Roc)
    nominacion = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField()
    moneda = models.CharField(max_length=25, default="cordobas", choices=MONEDAS)

#########################

class SMS(models.Model):
    numero = models.CharField(max_length=14)
    texto = models.CharField(max_length=240)
    enviado = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s-%s" % (self.numero, self.texto)

    def to_json(self):
        return {'numero': self.numero, 'texto': self.texto}


def send_sms(texto, numero):
    m = SMS(numero=numero, texto=texto)
    m.save()
    return m


class Preventa(models.Model):
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateTimeField(auto_now_add=True)


class Orden(models.Model):
    preventa = models.ForeignKey(Preventa)
    producto = models.ForeignKey(Producto)
    cantidad = models.FloatField()


class Modelo(models.Model):
    serie = models.CharField(max_length=5, null=True, blank=True)
    modelo = models.CharField(max_length=65)
    manual = models.FileField(upload_to="media",null=True, blank=True)

    def to_json(self):
        return {'serie': self.serie,
        'modelo': self.modelo,
        'errores': [x.to_json() for x in Codigo.objects.filter(tipo="er", modelo=self)],
        'trabas': [x.to_json() for x in Codigo.objects.filter(tipo="jm", modelo=self)],
        }

class Codigo(models.Model):
    modelo = models.ForeignKey(Modelo)
    TIPOS = (
    ("er", "Codigo de Error"),
    ("jm", 'Codigo de Traba'),
    )
    tipo = models.CharField(max_length=2, choices=TIPOS, default="er")
    codigo = models.CharField(max_length=9)
    short_description = models.CharField(max_length=125)
    details = models.TextField(max_length=1500, null=True, blank=True)

    def to_json(self):
        return {'codigo': self.codigo,
        'short_description': self.short_description,
        'details': self.details}


###########################################################################################


TIPOS_CUENTA = (
    ("ACTIVO", "ACTIVO"),
    ("PASIVO", "PASIVO"),
    ("CAPITAL", "CAPITAL"),
    ("INGRESO", "INGRESO"),
    ("EGRESO", "EGRESO"),
)

class Cuenta(models.Model):
    tipo = models.CharField(max_length=10, choices=TIPOS_CUENTA)
    codigo = models.CharField(max_length=14, null=True)
    nombre = models.CharField(max_length=400)
    operativa = models.BooleanField(default=True)
    cuenta = models.ForeignKey('self', null=True, related_name="cuenta_padre",
        blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.codigo, self.nombre)

    def buscar_padre(self):
        cuenta = None
        if self.codigo:
            if len(self.codigo) == 4:
                try:
                    cuenta = Cuenta.objects.get(codigo=self.codigo[:2])
                except Exception as e:
                    pass
            elif len(self.codigo) == 6:
                try:
                    return Cuenta.objects.get(codigo=self.codigo[:4])
                except Exception as e:
                    pass
            elif len(self.codigo) == 9:
                try:
                    return Cuenta.objects.get(codigo=self.codigo[:6])
                except Exception as e:
                    pass
            else:
                return None
        else:
            return cuenta

    def inactivar_padre(self):
        if self.cuenta and self.cuenta.operativa:
            self.cuenta.operativa = False
            self.cuenta.save()

    def prueba(self):
        return "padre %s" % str(self.codigo[:4])
    prueba.allow_tags = True

    def save(self, *args, **kwargs):
        self.cuenta = self.buscar_padre()
        if self.cuenta:
            self.inactivar_padre()
        super(Cuenta, self).save()


class manager_cuenta_credito(models.Manager):
    def get_queryset(self):
        ocupados = Cliente.objects.filter(cuenta_credito__isnull=False).values_list('cuenta_credito', flat=True)
        return super(manager_cuenta_credito, self).get_queryset().filter(codigo__startswith="112101",
            operativa=True).exclude(id__in=ocupados)


class cuenta_credito(Cuenta):
    objects = models.Manager()
    objects = manager_cuenta_credito()
    class Meta:
        proxy = True


def is_none(v):
    if v:
        return v
    else:
        return 0.0

def total_ventas(fecha, moneda):
    if moneda == "cordobas":
        try:
            return Factura.objects.filter(date__month=fecha.month, moneda=moneda).aggregate(Sum('total'))['total__sum'] + \
            cordobizar(Factura.objects.filter(date__month=fecha.month, moneda="dolares").aggregate(Sum('total'))['total__sum'])
        except Exception as e:
            return 0.0

    else:
        try:
            return Factura.objects.filter(date__month=fecha.month, moneda=moneda).aggregate(Sum('total'))['total__sum'] + \
            dolarizar(Factura.objects.filter(date__month=fecha.month, moneda="cordobas").aggregate(Sum('total'))['total__sum'])
        except Exception as e:
            return 0.0

def ventas():
    hoy = datetime.now()
    data = []
    for n in range(0, 6):
        data.append({'mes': hoy.month, 'ventas': total_ventas(hoy, "cordobas")})
        hoy = hoy - timedelta(days=30)
    return sorted(data, key=lambda x: x['mes'])

def iva_pendiente():
    iva = Factura.objects.filter(dec_iva=False, moneda="cordobas").aggregate(Sum('iva'))['iva__sum']
    if not iva:
        iva = 0.0
    for f in Factura.objects.filter(dec_iva=False, moneda="dolares"):
        iva += cordobizar(f.iva, f.date)
    return iva

def ingresos_categoria():
    cordobas = Factura.objects.filter(tipo='venta', dec_iva=False, moneda="cordobas")
    dolares = Factura.objects.filter(tipo='venta', dec_iva=False, moneda="dolares")
    dcor = Detalle.objects.filter(factura__in=cordobas)
    ddol = Detalle.objects.filter(factura__in=dolares)
    cats = Detalle.objects.filter(factura__in=Factura.objects.filter(
    tipo='venta', dec_iva=False)).distinct('producto')
    data = []
    for c in cats:
        data.append({'name': c.producto.name,
        'total': is_none(dcor.filter(producto=c.producto).annotate(
            total_producto=F('cantidad')*F('price')).aggregate(
                Sum('total_producto'))['total_producto__sum']) +
                cordobizar(is_none(ddol.filter(producto=c.producto).annotate(
                total_producto=F('cantidad')*F('price')).aggregate(
                Sum('total_producto'))['total_producto__sum']))
        })
    return data

def egresos_categoria():
    cordobas = Factura.objects.filter(tipo='compra', dec_iva=False, moneda="cordobas")
    dolares = Factura.objects.filter(tipo='compra', dec_iva=False, moneda="dolares")
    dcor = Detalle.objects.filter(factura__in=cordobas)
    ddol = Detalle.objects.filter(factura__in=dolares)
    cats = Detalle.objects.filter(factura__in=Factura.objects.filter(
    tipo='compra', dec_iva=False)).distinct('producto')
    data = []
    for c in cats:
        data.append({'name': c.producto.name,
        'total': is_none(dcor.filter(producto=c.producto).annotate(
            total_producto=F('cantidad')*F('price')).aggregate(
                Sum('total_producto'))['total_producto__sum']) +
                cordobizar(is_none(ddol.filter(producto=c.producto).annotate(
                total_producto=F('cantidad')*F('price')).aggregate(
                Sum('total_producto'))['total_producto__sum']))
        })
    return data

def impuestos():
    compras_cordobas = Factura.objects.filter(tipo='compra', dec_iva=False, moneda="cordobas")
    compras_dolares = Factura.objects.filter(tipo='compra', dec_iva=False, moneda="dolares")
    ventas_cordobas = Factura.objects.filter(tipo='venta', dec_iva=False, moneda="cordobas")
    ventas_dolares = Factura.objects.filter(tipo='venta', dec_iva=False, moneda="dolares")

    iva_acreditable = is_none(compras_cordobas.filter(excento_iva=False).aggregate(Sum('iva'))['iva__sum']) + \
    cordobizar(is_none(compras_dolares.filter(excento_iva=False).aggregate(Sum('iva'))['iva__sum']))

    iva_debitable = is_none(ventas_cordobas.filter(excento_iva=False).aggregate(Sum('iva'))['iva__sum']) + \
    cordobizar(is_none(ventas_dolares.filter(excento_iva=False).aggregate(Sum('iva'))['iva__sum']))

    data = [{'name': 'IVA ACREDITABLE', 'total': iva_acreditable}, {'name': 'IVA POR PAGAR', 'total': iva_debitable}]
    return data

def ventas_cliente():
    data = []
    images = None
    data.append(("Cliente", "Ventas"))
    ventas_cordobas = Factura.objects.filter(tipo='venta', dec_iva=False, moneda="cordobas")
    ventas_dolares = Factura.objects.filter(tipo='venta', dec_iva=False, moneda="dolares")
    clientes = Factura.objects.filter(tipo='venta', dec_iva=False).distinct('cliente')
    for c in clientes:
        data.append((c.cliente.name,
        is_none(ventas_cordobas.filter(cliente=c.cliente).aggregate(Sum('subtotal'))['subtotal__sum'])
        +
        cordobizar(is_none(ventas_dolares.filter(cliente=c.cliente).aggregate(Sum('subtotal'))['subtotal__sum']))
        ))
    return data, images

def catalogo_productos():
    ps = Producto.objects.filter(vender=True)
    data = []
    data.append(('Codigo', 'Descripcion', 'Precio', 'Costo', 'Existencia', 'Imagen'))
    images = []
    for p in ps:
        data.append((p.code, p.name, p.price, p.cost, p.existencia_total(), ''))
        if p.imagen:
            images.append(p.imagen.path)
        else:
            images.append('')
    return data, images
