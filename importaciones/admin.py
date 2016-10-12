from django.contrib import admin
from .models import *


class item_admin(admin.TabularInline):
    model = Item
    extra = 0

class importacion_admin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('nombre', 'estado')
    change_form_template = "admin/importacion.html"
    list_filter = ('estado', )
    inlines = [item_admin,]
    fields = (('nombre', 'fecha', 'estado'), 'blog', ('proforma_proveedor',
        'proforma'), ('flete', 'aduanas'), ('divisa', 'banco'))

admin.site.register(Importacion, importacion_admin)
