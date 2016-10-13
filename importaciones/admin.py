from django.contrib import admin
from .models import *
from .forms import ImportacionForm, ItemForm

class item_admin(admin.TabularInline):
    form  = ItemForm
    model = Item
    extra = 0
    fields = ('cantidad', 'descripcion', 'fob', 'cif', 'cip', 'precio', 'anexo')

class importacion_admin(admin.ModelAdmin):
    form = ImportacionForm
    date_hierarchy = 'fecha'
    list_display = ('nombre', 'estado')
    change_form_template = "admin/importacion.html"
    list_filter = ('estado', )
    inlines = [item_admin,]
    fields = (('nombre', 'fecha', 'estado'), 'blog',
                ('proforma_proveedor', 'proforma', 'guia'),
                ('pais', 'divisa', 'aduanas', 'factor'),
                ('peso', 'banco'),
                ('flete', 'otros', 'total_fob', 'utilidad'))

admin.site.register(Importacion, importacion_admin)

class tarifa_zona(admin.TabularInline):
    model = Tarifa
    extra = 0

class zona_admin(admin.ModelAdmin):
    inlines = [tarifa_zona,]

admin.site.register(Zona, zona_admin)


class pais_admin(admin.ModelAdmin):
    list_display = ('nombre', 'zona')

admin.site.register(Pais, pais_admin)
