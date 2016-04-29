from __future__ import unicode_literals
from base.models import Entidad
from django.db import models


class Marca(Entidad):
    pass


class Modelo(Entidad):
    marca = models.ForeingKey(Marca)


class Equipo(Entidad):
    marca = models.ForeingKey(Marca)
    modelo = models.ForeingKey(Modelo)
    serie = models.CharField(max_lenght=25)
    costo = models.FloatField()
    contador = models.PositiveIntegerField()


class Cliente(Entidad):
    identificacion = models.CharField(max_lenght=14)
    telefono = models.CharField(max_lenght=40, null=True, blank=True)
    direccion = models.TextField(max_lenght=400, null=True, blank=True)
    contacto = models.CharField(max_lenght=100, null=True, blank=True)


class Area(Entidad):
    cliente = models.ForeingKey(Cliente)
    contacto = models.CharField(max_lenght=100, blank=True, null=True)
