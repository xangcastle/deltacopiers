from __future__ import unicode_literals
from base.models import Entidad
from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from jsonfield import JSONField
from django.forms.models import model_to_dict


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

    def detalles(self):
        return DetalleGestion.objects.filter(tipo_gestion=self)

    def to_json(self):
        obj = model_to_dict(self)
        obj['campos'] = []
        for d in self.detalles():
            o = model_to_dict(d)
            if d.elementos():
                o['elementos'] = []
                for e in d.elementos():
                    o['elementos'].append(model_to_dict(e))
            obj['campos'].append(o)
        return obj

    class Meta:
        verbose_name_plural = "tipos de gestiones"


TIPOS = (
('input', 'input'),
('radio', 'radio'),
('textarea', 'textarea'),
('combobox', 'combobox'),
('checkbox', 'checkbox'),
)

class DetalleGestion(models.Model):
    tipo_gestion = models.ForeignKey(TipoGestion)
    tipo = models.CharField(max_length=25, choices=TIPOS, verbose_name="tipo de campo")
    requerido = models.BooleanField(default=True)
    titulo = models.CharField(max_length=65, verbose_name="titulo a mostrar")
    nombreVariable = models.CharField(max_length=65, verbose_name="nombre de la variable")
    habilitado = models.BooleanField(default=True)

    def elementos(self):
        return Elemento.objects.filter(combo=self.id)

    def __unicode__(self):
        return "%s - %s" % (self.tipo_gestion.name, self.nombreVariable)

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
    valor = models.CharField(max_length=65)


class Gestion(models.Model):
    destinatario = models.CharField(max_length=125, null=True)
    direccion = models.TextField(max_length=255, null=True)
    departamento = models.ForeignKey(Departamento, null=True)
    municipio = models.ForeignKey(Municipio, null=True)
    barrio = models.ForeignKey(Barrio, null=True)
    zona = models.ForeignKey(Zona, null=True)
    tipo_gestion = models.ForeignKey(TipoGestion)
    user = models.ForeignKey(User, null=True, blank=True)
    realizada = models.BooleanField(default=False)
    position = GeopositionField(null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    fecha_asignacion = models.DateField(null=True, blank=True)
    json = JSONField(null=True, blank=True)

    def to_json(self):
        o = {}
        o['destinatario'] = self.destinatario
        o['direccion'] = self.direccion
        o['departamento'] = self.departamento.name
        o['municipio'] = self.municipio.name
        o['barrio'] = self.barrio.name
        o['zona'] = self.zona.name
        o['tipo_gestion'] = self.tipo_gestion.name
        o['tipo_gestion_id'] = self.tipo_gestion.id
        if self.position:
            o['latitude'] = self.position.latitude
            o['longitude'] = self.position.longitude
        return o

    class Meta:
        verbose_name_plural = "gestiones"
