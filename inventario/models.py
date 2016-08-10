from __future__ import unicode_literals

from django.db import models


AFECTACIONES = (
(1, "POSITIVA"),
(-1, "NEGATIVA"),
(0, "SIN AFECTACION"),
)


class TipoDoc(models.Model):
    name = models.CharField(max_length=65)
    afectacion = models.IntegerField(choices=AFECTACIONES)

    def __unicode__(self):
        return "%s" % (self.name)

class Cliente(models.Model):
    name = models.CharField(max_length=65)
    identificacion = models.CharField(max_length=14, help_text="numero ruc")
    direccion = models.TextField(max_length=255)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=125)


class Documento(models.Model):
    numero = models.PositiveIntegerField()
    tipo = models.ForeignKey(TipoDoc)
    fecha = models.DateTimeField()
    cliente = models.ForeignKey(Cliente)


class Detalle(models.Model):
    documento = models.ForeignKey(Documento, null=True)
    producto = models.ForeignKey('Producto')
    cantidad = models.FloatField()
    precio = models.FloatField()
    costo = models.FloatField()
    existencia = models.FloatField()
    saldo = models.FloatField()


class Producto(models.Model):
    barra = models.CharField(max_length=65)
    nombre = models.CharField(max_length=65)
    precio = models.FloatField()
    costo = models.FloatField()
