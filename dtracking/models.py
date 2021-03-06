from __future__ import unicode_literals
from base.models import Entidad
from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from jsonfield import JSONField
from datetime import datetime
from moneycash.models import send_sms as wiliam_sms
import json


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
    intervalo = models.PositiveIntegerField(null=True, verbose_name="intervalo de seguimiento",
    help_text="esto determina que tan seguido el gestor reportara su posicion gps en segundos")

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
        o['intervalo'] = self.intervalo
        return o

    class Meta:
        verbose_name_plural = "gestores"


class Departamento(Entidad):
    pass


class Municipio(Entidad):
    departamento = models.ForeignKey(Departamento)


class Barrio(Entidad):
    municipio = models.ForeignKey(Municipio)

    def referencias(self):
        return Gestion.objects.filter(barrio=self).values_list('direccion', flat=True)[:5]


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
        for d in self.detalles().order_by('orden'):
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
    orden = models.IntegerField(null=True, blank=True)

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
        ordering =['orden', ]


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
    barra = models.CharField(max_length=65, null=True)
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
    fecha_vence = models.DateField(null=True, blank=True)
    json = JSONField(null=True, blank=True)
    observaciones = models.TextField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.tipo_gestion.name, self.destinatario)

    def cargar_archivo(self, archivo, variable):
        a, created = Archivo.objects.get_or_create(gestion=self,
        variable=variable)
        a.archivo = archivo
        a.save()
        return a

    def media(self):
        return Archivo.objects.filter(gestion=self)

    def to_json(self):
        o = {}
        o['id'] = self.id
        o['destinatario'] = self.destinatario
        o['direccion'] = self.direccion
        o['telefono'] = self.telefono
        o['departamento'] = self.departamento.name
        o['municipio'] = self.municipio.name
        o['barrio'] = self.barrio.name
        o['barra'] = self.barra
        if self.zona:
            o['zona'] = self.zona.name
        else:
            o['zona'] = ""
        o['tipo_gestion'] = self.tipo_gestion.id
        if self.position:
            o['latitude'] = str(self.position.latitude)
            o['longitude'] = str(self.position.longitude)
        if self.media():
            o['media'] = []
            for a in self.media():
                o['media'].append(a.to_json())
        if self.json:
            o['data'] = self.json
        return o

    def numero_gestor(self):
        return Gestor.objects.get(user=self.user).numero

    def _realizada(self):
        if self.realizada:
            return '<a data-id="%s" class="detalle">Ver&nbsp;<img src="/static/admin/img/icon-yes.svg" alt="True"></a>' \
            % self.id
        else:
            return '<img src="/static/admin/img/icon-no.svg" alt="False">'
    _realizada.allow_tags = True
    _realizada.short_description = "Realizada"

    class Meta:
        verbose_name_plural = "gestiones"


class Archivo(models.Model):
    gestion = models.ForeignKey(Gestion)
    variable = models.CharField(max_length=80)
    archivo = models.FileField(null=True)

    def __unicode__(self):
        return "%s %s" % (self.gestion, self.archivo)

    def to_json(self):
        return {'variable': self.variable,
        'archivo': self.archivo.url}

    class Meta:
        verbose_name_plural = "Archivos Media"


class Position(models.Model):
    user = models.ForeignKey(User)
    position = GeopositionField()
    fecha = models.DateTimeField()

    def to_json(self):
        return {
        'label': self.user.username[0].upper(),
        'usuario': self.user.username,
        'latitude': self.position.latitude,
        'longitude': self.position.longitude,
        'fecha': str(self.fecha),
        }

    class Meta:
        verbose_name = 'posicion'
        verbose_name_plural = "seguimiento gps"


class Import(models.Model):
    destinatario = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.TextField(max_length=250, null=True, blank=True)
    telefono = models.CharField(max_length=65, null=True, blank=True)
    barrio = models.CharField(max_length=150, null=True, blank=True)
    municipio = models.CharField(max_length=150, null=True, blank=True)
    departamento = models.CharField(max_length=150, null=True, blank=True)
    idbarrio = models.ForeignKey('Barrio', null=True, blank=True,
        db_column='idbarrio', verbose_name='barrio')
    iddepartamento = models.ForeignKey('Departamento', null=True, blank=True,
        db_column='iddepartamento', verbose_name='departamento')
    idmunicipio = models.ForeignKey('Municipio', null=True, blank=True,
        db_column='idmunicipio', verbose_name='municipio')

    def __unicode__(self):
        return "%s - %s" % (self.destinatario, self.direccion)

    def get_departamento(self):
        d = None
        if self.departamento:
            try:
                d = Departamento.objects.get(name_alt=self.departamento)
            except:
                d, created = Departamento.objects.get_or_create(
                    name=self.departamento)
        return d

    def get_municipio(self):
        m = None
        try:
            if self.municipio and self.iddepartamento:
                m = Municipio.objects.get(departamento=self.iddepartamento,
                    name_alt=self.municipio)
        except:
            m, created = Municipio.objects.get_or_create(
                departamento=self.iddepartamento, name=self.municipio)
        return m

    def get_barrio(self):
        b = None
        try:
            if self.barrio and self.idmunicipio and self.iddepartamento:
                b, created = Barrio.objects.get_or_create(
                municipio=self.idmunicipio, name=self.barrio)
        except:
            b = Barrio.objects.filter(municipio=self.idmunicipio,
            name=self.barrio)[0]
        return b

    def integrar_registro(self, fecha_asignacion, fecha_vence, tipo_gestion, eliminar=False):
        g = Gestion()
        g.destinatario = self.destinatario
        g.direccion = self.direccion
        g.telefono = self.telefono
        g.barrio = self.idbarrio
        g.municipio = self.idmunicipio
        g.departamento = self.iddepartamento
        g.zona = get_zona(self.idbarrio)
        g.user = get_user(g.zona)
        g.fecha_asignacion = fecha_asignacion
        g.fecha_vence = fecha_vence
        g.tipo_gestion = tipo_gestion
        g.save()
        if eliminar:
            self.delete()

def get_zona(barrio):
    try:
        return Zona.objects.get(
            id=zona_barrio.objects.filter(barrio=barrio)[0].zona.id)
    except:
        return None

def get_user(zona):
    try:
        user = None
        for g in Gestor.objects.all():
            if zona in g.zonas.all():
                user = g.user
        return user
    except:
        return None


def autoasignacion(gestiones):
    for g in gestiones:
        if not g.zona:
            g.zona = get_zona(g.barrio)
        g.user = get_user(g.zona)
        g.fecha_asignacion = datetime.now()
        g.save()


def integrar(ps):
    message = ""
    ds = ps.order_by('departamento').distinct('departamento')
    for d in ds:
        qs = ps.filter(departamento=d.departamento)
        qs.update(iddepartamento=d.get_departamento().id)
    ms = ps.order_by('departamento', 'municipio').distinct(
        'departamento', 'municipio')
    for m in ms:
        qs = ps.filter(departamento=m.departamento,
            municipio=m.municipio)
        qs.update(idmunicipio=m.get_municipio().id)
    bs = ps.order_by('departamento', 'municipio', 'barrio').distinct(
        'departamento', 'municipio', 'barrio')
    for b in bs:
        qs = ps.filter(departamento=b.departamento,
            municipio=b.municipio, barrio=b.barrio)
        qs.update(idbarrio=b.get_barrio().id)
    message += "integrado, total de gestiones = %s end %s departamentos" \
    % (str(ps.count()), str(ds.count()))
    return message


class SMS(models.Model):
    user = models.ForeignKey(User, null=True)
    texto = models.CharField(max_length=540)
    enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True)

    def __unicode__(self):
        return "%s" % (self.texto)

    def to_json(self):
        return {'texto': self.texto}


def send_sms(texto):
    m = SMS(texto=texto)
    m.save()
    return m

def cancelar_gestiones(gestiones, motivo=""):
    usuarios = gestiones.filter(user__isnull=False).order_by('user').distinct('user')
    for u in usuarios:
        gs = gestiones.filter(user=u.user)
        ids = gs.values_list('id', flat=True)
        ids = '[' + ','.join([str(x) for x in ids]) + ']'
        texto = 'MEN{"g":%s,"c":"%s","m":"%s"}MEN' % (ids, u.user.id,
        ("%s gestiones eliminadas" % gs.count()))
        wiliam_sms(texto, gs[0].numero_gestor())
    gestiones.update(realizada=True, observaciones=motivo)
