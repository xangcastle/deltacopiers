# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .middlewares import get_current_user


class datos_generales(models.Model):
    identificacion = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="ruc/cedula")
    telefono = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


def get_code(entidad):
        model = type(entidad)
        code = ''
        sets = model.objects.all()
        if sets:
            maxi = str(sets.aggregate(Max('code'))['code__max'])
            if maxi:
                consecutivo = list(range(1, int(maxi)))
                ocupados = list(sets.values_list('code',
                flat=True))
                n = 0
                for l in ocupados:
                    ocupados[n] = int(str(l))
                    n += 1
                disponibles = list(set(consecutivo) - set(ocupados))
                if len(disponibles) > 0:
                    code = min(disponibles)
                else:
                    code = max(ocupados) + 1
        return str(code).zfill(4)


class Entidad(models.Model):
    code = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="codigo", unique=True)
    name = models.CharField(max_length=100, verbose_name="nombre")
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.code and self.name:
            return str(self.code) + " " + self.name
        elif self.name:
            return self.name
        elif self.code:
            return str(self.code)
        else:
            return ''

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = get_code(self)
        super(Entidad, self).save()

    class Meta:
        abstract = True
        ordering = ['code']


class Periodo(models.Model):
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    inicio_produccion = models.DateField(null=True, blank=True)
    fin_produccion = models.DateField(null=True, blank=True)
    inicio_ventas = models.DateField(null=True, blank=True)
    fin_ventas = models.DateField(null=True, blank=True)
    cerrado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.fecha_inicial.strftime("%B %Y")

    def short_name(self):
        return self.fecha_inicial.strftime("%B %Y")

    class Meta:
        ordering = ['-fecha_final']


class Sucursal(Entidad):
    pass


class Cuenta(Entidad):
    saldo = models.FloatField(default=0)


class cuenta_periodo(models.Model):
    periodo = models.ForeignKey(Periodo)
    cuenta = models.ForeignKey(Cuenta)
    saldo_inicial = models.FloatField(default=0)
    saldo_final = models.FloatField(default=0)


class Movimiento(models.Model):
    comprobante = models.ForeignKey('Comprobante')
    cuenta = models.ForeignKey(Cuenta)
    debe = models.FloatField(default=0)
    haber = models.FloatField(default=0)


class TipoDoc(Entidad):
    tipos_de_afectacion = ((1, 'POSITIVA'), (-1, 'NEGATIVA'),
        (0, 'SIN AFECTACION'))
    contabiliza = models.BooleanField(default=True)
    afectation = models.IntegerField(choices=tipos_de_afectacion)


class Numeracion(models.Model):
    tipodoc = models.ForeignKey(TipoDoc)
    sucursal = models.ForeignKey(Sucursal)
    numero_inicial = models.PositiveIntegerField(default=1)


class Documento(models.Model):
    fecha = models.DateTimeField()
    numero = models.PositiveIntegerField(null=True, blank=True)
    tipodoc = models.ForeignKey(TipoDoc, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_documento")
    periodo = models.ForeignKey(Periodo, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_periodo")
    user = models.ForeignKey(User, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_user")
    sucursal = models.ForeignKey(Sucursal, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_sucursal")
    autorizado = models.BooleanField(default=True)
    impreso = models.BooleanField(default=False)
    contabilizado = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)

    def __unicode__(self):
        if self.numero:
            return type(self).__name__ + " " + str(self.numero)
        else:
            return type(self).__name__

    class Meta:
        ordering = ['-numero']
        abstract = True

    def get_fecha_inicial(self, fecha):
        return datetime(fecha.year, fecha.month, 0o1)

    def get_fecha_final(self, fecha):
        if fecha.month == 12:
            return datetime(fecha.year + 1, 0o1, 0o1) - timedelta(days=1)
        else:
            return datetime(fecha.year,
                fecha.month + 1, 0o1) - timedelta(days=1)

    def get_periodo(self, fecha):
        p, created = Periodo.objects.get_or_create(
            fecha_inicial=self.get_fecha_inicial(fecha),
            fecha_final=self.get_fecha_final(fecha))
        return p

    def get_numero(self):
        return 0

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = datetime.now()
        self.periodo = self.get_periodo(self.fecha)
        if not self.numero:
            self.numero = self.get_numero()
        try:
            if not self.user:
                self.user = get_current_user()
        except:
            self.user = User.objects.all().order_by('id')[0]
        super(Documento, self).save()


