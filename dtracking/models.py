from __future__ import unicode_literals
from base.models import Entidad
from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from jsonfield import JSONField
from datetime import datetime


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
        o['zona'] = self.zona.name
        o['tipo_gestion'] = self.tipo_gestion.id
        if self.position:
            o['latitude'] = str(self.position.latitude)
            o['longitude'] = str(self.position.longitude)
        if self.media():
            o['media'] = []
            for a in self.media():
                o['media'].append(str(a.archivo.url))
        return o

    class Meta:
        verbose_name_plural = "gestiones"


class Archivo(models.Model):
    gestion = models.ForeignKey(Gestion)
    variable = models.CharField(max_length=80)
    archivo = models.FileField(null=True)

    def __unicode__(self):
        return "%s %s" % (self.gestion, self.archivo)

    class Meta:
        verbose_name_plural = "Archivos Media"


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
                departamento=self.iddepartamento,
                municipio=self.idmunicipio, name=self.barrio)
        except:
            b = Barrio.objects.filter(departamento=self.iddepartamento,
                municipio=self.idmunicipio, name=self.barrio)[0]
        return b

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
    message += "integrado, total de facturas = %s end %s departamentos" \
    % (str(ps.count()), str(ds.count()))
    return message
