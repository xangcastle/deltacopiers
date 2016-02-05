# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max
from import_export.admin import ImportExportModelAdmin


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
        verbose_name="codigo")
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
        ordering = ['name']


class entidad_admin(ImportExportModelAdmin):
    list_display = ('code', 'name')
    actions = ['activar', 'inactivar']
    ordering = ('code',)
    search_fields = ('code', 'name')
    ordering = ('name',)

    def inactivar(self, request, queryset):
        queryset.update(activo=False)
    inactivar.short_description = "Desactivar selected objects"

    def activar(self, request, queryset):
        queryset.update(activo=True)
    activar.short_description = "Activar selected objects"


