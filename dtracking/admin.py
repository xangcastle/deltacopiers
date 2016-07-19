from django.contrib import admin
from base.admin import entidad_admin
from .models import *


class detalle_tabular(admin.TabularInline):
    model = DetalleGestion
    extra = 0
    fields = ('nombreVariable', 'tipo', 'titulo', 'habilitado', 'requerido')


class tipoGestion_admin(entidad_admin):
    inlines = [detalle_tabular,]


class gestion_admin(admin.ModelAdmin):
    list_display = ('tipo_gestion', 'user', 'realizada', 'fecha')


class elemento_admin(admin.ModelAdmin):
    list_display = ('valor', 'combo')
    list_filter = ('combo',)

admin.site.register(Gestion, gestion_admin)
admin.site.register(TipoGestion, tipoGestion_admin)
admin.site.register(Departamento, entidad_admin)
admin.site.register(Municipio, entidad_admin)
admin.site.register(Barrio, entidad_admin)
admin.site.register(Zona, entidad_admin)
admin.site.register(Elemento, elemento_admin)
