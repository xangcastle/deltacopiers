from __future__ import unicode_literals

from django.db import models
from base.models import Entidad
from django.forms.models import model_to_dict
#from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum

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
        return Factura.objects.filter(cliente=self)

    def to_json(self):
        obj = super(Cliente, self).to_json()
        obj['facturas'] = []
        for f in self.facturas():
            obj['facturas'].append(model_to_dict(f))
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

    def existencias(self):
        return Existencia.objects.filter(producto=self)

    def url_imagen(self):
        if self.imagen:
            return self.imagen.url
        else:
            return "#"

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.imagen)
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


class Factura(models.Model):
    user = models.ForeignKey(User, null=True,
        related_name="moneycash_factura_user")
    date = models.DateTimeField(auto_now_add=True)
    numero = models.PositiveIntegerField(null=True)
    cliente = models.ForeignKey(Cliente, null=True)
    subtotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    iva = models.FloatField(null=True)
    retension = models.FloatField(null=True)
    total = models.FloatField(null=True)
    excento_iva = models.NullBooleanField()
    aplica_ir = models.NullBooleanField()
    aplica_al = models.NullBooleanField()
    impresa = models.BooleanField(default=False)

    def to_json(self):
        obj = model_to_dict(self)
        obj['cliente_data'] = self.cliente.to_json()
        return obj


class Detalle(models.Model):
    factura = models.ForeignKey(Factura)
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    cantidad = models.FloatField()
    price = models.FloatField()
    discount = models.FloatField(null=True)
    cost = models.FloatField()


class Salida(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    concepto = models.TextField(max_length=300, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    user_solicita = models.ForeignKey(User, null=True,
        related_name="user_solicita")
    user_entrega = models.ForeignKey(User, null=True,
        related_name="user_entrega")
    user_autoriza = models.ForeignKey(User, null=True,
        related_name="user_autoriza")

    def __unicode__(self):
        return "salida # " + srt(self.numero)

    def detalle(self):
        return salidaDetalle.objects.filter(salida=self)

class salidaDetalle(models.Model):
    salida = models.ForeignKey(Salida)
    producto = models.ForeignKey(Producto)
    cantidad = models.FloatField()
    costo = models.FloatField(null=True)
