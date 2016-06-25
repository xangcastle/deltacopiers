from __future__ import unicode_literals
from base.models import Entidad
from django.db import models


class Marca(Entidad):
    pass


class Modelo(Entidad):
    marca = models.ForeignKey(Marca)


class Equipo(Entidad):
    marca = models.ForeignKey(Marca)
    modelo = models.ForeignKey(Modelo)
    serie = models.CharField(max_length=25)
    costo = models.FloatField()
    contador_inicial = models.PositiveIntegerField()
    contador_actual = models.PositiveIntegerField()
    vida_util = models.PositiveIntegerField()


class Cliente(Entidad):
    identificacion = models.CharField(max_length=14)
    telefono = models.CharField(max_length=40, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank=True)


class Area(Entidad):
    cliente = models.ForeignKey(Cliente)
    contacto = models.CharField(max_length=100, blank=True, null=True)


class Periodo(models.Model):
    inicio_contable = models.DateField()
    cierre_contable = models.DateField()
    inicio_produccion = models.DateField()
    cierre_produccion = models.DateField()


class Recibo(models.Model):
    numero = models.PositiveIntegerField()
    area = models.ForeignKey(Area)
    fecha = models.DateField()
    periodo = models.ForeignKey(Periodo)


class ReciboDetalle(models.Model):
    recibo = models.ForeignKey(Recibo)
    equipo = models.ForeignKey(Equipo)
    contador_inicial = models.PositiveIntegerField()
    contador_final = models.PositiveIntegerField()
    total_copias = models.PositiveIntegerField()
    precio = models.FloatField()


class Servicio(Entidad):
    tarifa = models.FloatField()


class Contrato(models.Model):
    area = models.ForeignKey(Area)
    precio = models.FloatField()
    equipo = models.ForeignKey(Equipo)
    cuenta = models.CharField(max_length=25)


class Corte(models.Model):
    fecha = models.DateField()
    periodo = models.ForeignKey(Periodo)
    equipo = models.ForeignKey(Equipo)
    contador_inicial = models.PositiveIntegerField()
    contador_final = models.PositiveIntegerField()


class DetalleCorte(models.Model):
    corte = models.ForeignKey(Corte)
    area = models.ForeignKey(Area)
    total = models.PositiveIntegerField()