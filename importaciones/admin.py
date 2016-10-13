from django.contrib import admin
from .models import *
from .forms import ImportacionForm

class item_admin(admin.TabularInline):
    model = Item
    extra = 0
    fields = ('cantidad', 'descripcion', 'fob', 'cif', 'cip', 'precio')

class importacion_admin(admin.ModelAdmin):
    form = ImportacionForm
    date_hierarchy = 'fecha'
    list_display = ('nombre', 'estado')
    change_form_template = "admin/importacion.html"
    list_filter = ('estado', )
    inlines = [item_admin,]
    fields = (('nombre', 'fecha', 'estado'), 'blog',
                ('proforma_proveedor', 'proforma'),
                ('total_fob', 'divisa', 'aduanas', 'factor'),
                ('flete', 'banco', 'otros', 'utilidad'))

admin.site.register(Importacion, importacion_admin)
