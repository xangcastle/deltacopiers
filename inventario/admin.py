from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class tipodoc_admin(admin.ModelAdmin):
    list_display = ('name', 'afectacion')
    list_filter = ('afectacion',)
    search_fields = ('name',)


class cliente_admin(ImportExportModelAdmin):
    list_display = ('name', 'identificacion', 'direccion', 'telefono', 'email')
    fields = (('name', 'identificacion'), 'direccion', ('telefono', 'email'))



class items(admin.TabularInline):
    model = Detalle
    extra = 1
    classes = ('grp-collapcse grp-open')

class Factura(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'fecha', 'cliente')
    inlines = [items,]

admin.site.register(TipoDoc, tipodoc_admin)
admin.site.register(Cliente, cliente_admin)
admin.site.register(Documento, Factura)
