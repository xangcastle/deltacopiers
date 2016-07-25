from __future__ import unicode_literals
from base.models import Entidad
from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from jsonfield import JSONField


CONECTIONS = (
('SMS + WIFI', 'SMS + WIFI'),
('3G + WIFI', '3G + WIFI'),
('WIFI', 'WIFI'),
)


class Gestor(models.Model):
    user = models.OneToOneField(User)
    numero = models.CharField(max_length=8, help_text="numero de celular")
    server_conection = models.CharField(max_length=25, choices=CONECTIONS,
    default='WIFI', null=True, blank=True)
    sms_gateway = models.CharField(max_length=20, null=True)
    foto = models.ImageField(null=True)
    zonas = models.ManyToManyField('Zona', null=True, blank=True)
    tipo_gestion = models.ManyToManyField('TipoGestion', null=True, blank=True)

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="60" />' % (self.foto)
    image_thumb.allow_tags = True
    image_thumb.short_description = "Imagen"

    def __unicode__(self):
        return str(self.user)

    def to_json(self):
        o = {}
        o['numero'] = self.numero
        o['foto'] = self.foto.url
        o['server_conection'] = self.server_conection
        if self.server_conection == 'SMS + WIFI':
            o['sms_gateway'] = self.sms_gateway
        o['zonas'] = []
        o['tipos_gestion'] = []
        for z in self.zonas.all():
            o['zonas'].append(z.name)
        for t in self.tipo_gestion.all():
            o['tipos_gestion'].append(t.name)
        return o

    class Meta:
        verbose_name_plural = "gestores"


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
        obj = {'id': self.id, 'name': self.name}
        obj['campos'] = []
        for d in self.detalles():
            obj['campos'].append(d.to_json())
        return obj

    class Meta:
        verbose_name_plural = "tipos de gestiones"


TIPOS = (
('input', 'input'),
('radio', 'radio'),
('textarea', 'textarea'),
('combobox', 'combobox'),
('checkbox', 'checkbox'),
('foto', 'foto'),
('firma', 'firma'),
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

    def to_json(self):
        o = {}
        o['tipo'] = self.tipo
        o['requerido'] = self.requerido
        o['titulo'] = self.titulo
        o['nombreVariable'] = self.nombreVariable
        o['habilitado'] = self.habilitado
        if self.elementos():
            o['elementos'] = []
        for e in self.elementos():
            o['elementos'].append({'id': e.id, 'valor': e.valor})
        return o


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
    telefono = models.CharField(max_length=65, null=True, blank=True)
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

    def __unicode__(self):
        return "%s - %s" % (self.tipo_gestion.name, self.destinatario)

    def to_json(self):
        o = {}
        o['id'] = self.id
        o['destinatario'] = self.destinatario
        o['direccion'] = self.direccion
        o['telefono'] = self.telefono
        o['departamento'] = self.departamento.name
        o['municipio'] = self.municipio.name
        o['barrio'] = self.barrio.name
        o['zona'] = self.zona.name
        o['tipo_gestion'] = self.tipo_gestion.id
        if self.position:
            o['latitude'] = str(self.position.latitude)
            o['longitude'] = str(self.position.longitude)
        return o

    class Meta:
        verbose_name_plural = "gestiones"
