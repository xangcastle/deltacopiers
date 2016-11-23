from django.contrib import admin
from .models import *
from .forms import ImportacionForm, ItemForm
from django.shortcuts import render_to_response
from django.template import RequestContext


class item_admin(admin.TabularInline):
    form  = ItemForm
    model = Item
    extra = 0
    fields = ('cantidad', 'descripcion', 'fob', 'cif', 'cip', 'precio', 'anexo')
    classes = ('grp-collapse grp-open',)

class importacion_admin(admin.ModelAdmin):
    form = ImportacionForm
    date_hierarchy = 'fecha'
    list_display = ('nombre', 'total_fob', 'utilidad', 'estado')
    change_form_template = "admin/importacion.html"
    list_filter = ('estado', )
    inlines = [item_admin,]

    fieldsets = (
        ('Datos Generales', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('nombre', 'fecha', 'estado'), 'blog')
        }),
        ('Documentacion y Costos', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('guia', 'banco', 'proforma_proveedor'),
                        ('pais', 'divisa', 'proforma'),
                        ('peso', 'aduanas', 'orden'),
                        ('flete', 'otros', 'plist')),
        }),
        ('Totales Agrabados', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('factor', ('total_cip', 'total_venta', 'utilidad')),
        })
    )

    def generar_proforma(self, request, queryset):
        context = RequestContext(request)
        context['queryset'] = queryset
        return render_to_response('admin/importaciones/proforma.html', context)
    actions = [generar_proforma,]

admin.site.register(Importacion, importacion_admin)

class tarifa_zona(admin.TabularInline):
    model = Tarifa
    extra = 0
    ordering = ('zona', 'precio')

class zona_admin(admin.ModelAdmin):
    inlines = [tarifa_zona,]

admin.site.register(Zona, zona_admin)


class pais_admin(admin.ModelAdmin):
    list_display = ('nombre', 'zona')

admin.site.register(Pais, pais_admin)
