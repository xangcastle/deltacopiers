from __future__ import unicode_literals

from django.db import models
from moneycash.models import MyUser


class base_cliente(models.Model):

    #datos del cliente
    cliente = models.ForeignKey('Cliente', null=True)
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    identificacion = models.CharField(max_length=14, null=True, blank=True,
        help_text="RUC/CEDULA")
    telefono = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=165, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)

    def estadisticas(self):
        return 0.25

    class Meta:
        abstract = True


class Factura(base_cliente):

    """
    Modelo factura. Cabezera de Documento
    """

    #datos del documento
    numero = models.CharField(max_length=25, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(MyUser, null=True)

    #totales del documento
    subtotal = models.FloatField(null=True, blank=True)
    descuento = models.FloatField(null=True, blank=True)
    iva = models.FloatField(null=True, blank=True)
    ir = models.FloatField(null=True, blank=True)
    al = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return 'Factura #' + str(self.numero)


class Detalle(models.Model):
    factura = models.ForeignKey(Factura)
    producto = models.ForeignKey('Producto', null=True)
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    cantidad = models.FloatField(null=True)
    precio = models.FloatField(null=True)
    iva = models.FloatField(null=True)

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Cliente(base_cliente):

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Producto(models.Model):
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    precio = models.FloatField(null=True)
    costo = models.FloatField(null=True)

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)