from django.contrib import admin
from base.admin import entidad_admin
from .models import *


class detalle_tabular(admin.TabularInline):
    model = DetalleGestion
    extra = 0
    fields = ('nombreVariable', 'tipo', 'titulo', 'habilitado', 'requerido')


class tipoGestion_admin(entidad_admin):
    inlines = [detalle_tabular,]

admin.site.register(TipoGestion, tipoGestion_admin)
admin.site.register(Departamento, entidad_admin)
admin.site.register(Municipio, entidad_admin)
admin.site.register(Barrio, entidad_admin)
