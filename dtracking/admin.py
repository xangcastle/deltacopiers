from django.contrib import admin
from base.admin import entidad_admin
from .models import *


class detalle_tabular(admin.TabularInline):
    model = DetalleGestion
    extra = 0
    fields = ('nombreVariable', 'tipo', 'titulo', 'habilitado', 'requerido',
    'orden')
    sortable_field_name = 'orden'


class tipoGestion_admin(entidad_admin):
    inlines = [detalle_tabular, ]


class gestion_admin(admin.ModelAdmin):
    list_display = ('destinatario', 'direccion', 'departamento', 'municipio',
    'barrio', 'tipo_gestion', 'user', 'realizada', 'fecha')
    list_filter = ('departamento', 'municipio', 'zona', 'realizada')
    search_fields = ('destinatario', 'departamento__name',
    'municipio__name', 'barrio__name', 'zona__name')


class elemento_admin(admin.ModelAdmin):
    list_display = ('valor', 'combo')
    list_filter = ('combo',)


class barrio_admin(entidad_admin):
    list_display = ('code', 'name', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('code', 'name', 'municipio__name',
    'municipio__departamento__name')


class gestor_admin(admin.ModelAdmin):
    list_display = ('user', 'numero', 'image_thumb')

admin.site.register(Gestion, gestion_admin)
admin.site.register(TipoGestion, tipoGestion_admin)
admin.site.register(Departamento, entidad_admin)
admin.site.register(Municipio, entidad_admin)
admin.site.register(Barrio, barrio_admin)
admin.site.register(Zona, entidad_admin)
admin.site.register(Elemento, elemento_admin)
admin.site.register(Gestor, gestor_admin)
