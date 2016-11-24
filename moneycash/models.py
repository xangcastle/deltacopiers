from __future__ import unicode_literals

from django.db import models
from base.models import Entidad
from django.forms.models import model_to_dict
#from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum, Max

#User = settings.AUTH_USER_MODEL


class TipoPago(Entidad):
    pass


class Sucursal(Entidad):
    pass


class Bodega(Entidad):
    sucursal = models.ForeignKey(Sucursal)


class Cliente(Entidad):
    ident = models.CharField(max_length=14, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=125, null=True, blank=True)
    address = models.TextField(max_length=400, null=True, blank=True)

    def facturas(self):
        return Documento.objects.filter(cliente=self)

    def saldo(self):
        return self.facturas().filter(saldo__gt=0.009).aggregate(Sum('saldo'))['saldo__sum']

    def to_json(self):
        obj = super(Cliente, self).to_json()
        obj['facturas'] = []
        for f in self.facturas():
            obj['facturas'].append(model_to_dict(f))
        obj['saldo'] = self.saldo()
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
    vender = models.NullBooleanField()
    comprar = models.NullBooleanField()
    almacenar = models.NullBooleanField()

    def existencias(self):
        return Existencia.objects.filter(producto=self)

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
        obj['imagen'] = self.url_imagen()
        obj['details'] = self.details
        obj['existencias'] = []
        for e in self.existencias():
            existencia = {'bodega': e.bodega.name, 'cantidad': e.cantidad, 'bodega_id': e.bodega.id}
            obj['existencias'].append(existencia)
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
    cantidad = models.FloatField()


TIPOS_AFECTACION = (
    ( 1, "POSITIVA"),
    ( 0, "SIN AFECTACION"),
    (-1, "NEGATIVA"),
    )


class TipoDoc(Entidad):
    contable = models.BooleanField(default=False)
    afectacion = models.IntegerField(default=0, choices=TIPOS_AFECTACION)
    afecta_costo = models.BooleanField(default=False)


class Documento(models.Model):
    tipodoc = models.ForeignKey(TipoDoc, null=True)
    sucursal = models.ForeignKey(Sucursal, null=True)
    user = models.ForeignKey(User, null=True,
        related_name="moneycash_factura_user")
    date = models.DateTimeField(auto_now_add=True)
    numero = models.PositiveIntegerField(null=True)
    cliente = models.ForeignKey(Cliente, null=True)
    subtotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    iva = models.FloatField(null=True)
    ir = models.FloatField(null=True)
    al = models.FloatField(null=True, verbose_name="alcaldia")
    total = models.FloatField(null=True)
    excento_iva = models.NullBooleanField()
    aplica_ir = models.NullBooleanField()
    aplica_al = models.NullBooleanField()
    tipopago = models.ForeignKey(TipoPago, null=True)
    impresa = models.BooleanField(default=False)
    saldo = models.FloatField(null=True)
    monto = models.FloatField(null=True)

    def to_json(self):
        obj = model_to_dict(self)
        obj['cliente_data'] = self.cliente.to_json()
        return obj

    def get_numero(self):
        try:
            return Documento.objects.filter(tipodoc=self.tipodoc).aggregate(Max('numero'))['numero__max'] + 1
        except:
            return 1



class Detalle(models.Model):
    documento = models.ForeignKey(Documento, null=True)
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    cantidad = models.FloatField()
    price = models.FloatField()
    discount = models.FloatField(null=True)
    cost = models.FloatField()
    existencia = models.FloatField(null=True)
    saldo = models.FloatField(null=True)
    costo_promedio = models.FloatField(null=True)

    def aplicar(self):
        pass

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
