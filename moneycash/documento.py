# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from import_export.admin import ImportExportModelAdmin
from django.db.models import Max
from .models import Periodo
from .middlewares import get_current_user


def get_numero(documento):
    sets = documento.__class__.objects.all()
    maxi = 0
    if sets:
        maxi += sets.aggregate(Max('numero'))['numero__max']
    numero = maxi + 1
    return numero


def get_fecha_inicial(fecha):
    return datetime(fecha.year, fecha.month, 0o1)


def get_fecha_final(fecha):
    if fecha.month == 12:
        return datetime(fecha.year + 1, 0o1, 0o1) - timedelta(days=1)
    else:
        return datetime(fecha.year, fecha.month + 1, 0o1) - timedelta(days=1)


def get_periodo(fecha):
    p, created = Periodo.objects.get_or_create(
        fecha_inicial=get_fecha_inicial(fecha),
        fecha_final=get_fecha_final(fecha))
    return p


class Documento(models.Model):
    fecha = models.DateField()
    numero = models.PositiveIntegerField(null=True, blank=True)
    periodo = models.ForeignKey(Periodo, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_periodo")
    user = models.ForeignKey(User, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_user")
    sucursal = models.ForeignKey('Sucursal', null=True, blank=True,
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

    def save(self, *args, **kwargs):
        self.periodo = get_periodo(self.fecha)
        if not self.numero:
            self.numero = get_numero(self)
        super(Documento, self).save()


class documento_admin(ImportExportModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('numero', 'fecha', 'user', 'sucursal',
        'impreso', 'entregado', 'contabilizado')
    list_filter = ('periodo', 'user', 'sucursal', 'impreso',
        'entregado', 'contabilizado')
    search_fields = ('numero',)