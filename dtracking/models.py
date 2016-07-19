from __future__ import unicode_literals
from base.models import Entidad
from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from jsonfield import JSONField


class Gestor(models.Model):
    user = models.OneToOneField(User)
    numero = models.CharField(max_length=8, help_text="numero de celular")
    foto = models.ImageField(null=True)
    zonas = models.ManyToManyField('Zona', null=True, blank=True)
    tipo_gestion = models.ManyToManyField('TipoGestion', null=True, blank=True)


class Departamento(Entidad):
    pass


class Municipio(Entidad):
    departamento = models.ForeignKey(Departamento)


class Barrio(Entidad):
    municipio = models.ForeignKey(Municipio)


class Zona(Entidad):
    departamento = models.ForeignKey(Departamento)


class ZonaBarrio(models.Model):
    zona = models.ForeignKey(Zona)
    barrio = models.ForeignKey(Barrio)
    orden = models.IntegerField(null=True, blank=True)


class TipoGestion(Entidad):
    pass


TIPOS = (
('input', 'input'),
('radio', 'radio'),
('textarea', 'textarea'),
('combobox', 'combobox'),
('checkbox', 'checkbox'),
)

class DetalleGestion(models.Model):
    tipo_gestion = models.ForeignKey(TipoGestion)
    tipo = models.CharField(max_length=25, choices=TIPOS)
    requerido = models.BooleanField(default=True)
    titulo = models.CharField(max_length=65)
    nombreVariable = models.CharField(max_length=65)
    habilitado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "campo"
        verbose_name_plural = "campos requeridos por la gestion"


class especiales(models.Manager):
    def get_queryset(self):
        return super(especiales, self).get_queryset().filter(tipo__in=['combobox', 'checkbox'])

class EspecialField(DetalleGestion):
    objects = models.Manager()
    objects = especiales()
    class Meta:
        proxy = True


class Elemento(models.Model):
    combo = models.ForeignKey(EspecialField)
    _id = models.IntegerField()
    _valor = models.CharField(max_length=65)


class Gestion(object):
    tipo_gestion = models.ForeignKey(TipoGestion)
    user = models.ForeignKey(User, null=True, blank=True)
    realizada = models.BooleanField(default=False)
    position = GeopositionField(null=True)
    fecha = models.DateTimeField()
    json = JSONField(null=True)
