from django.contrib import admin
from .models import *


class factura_detalle(admin.TabularInline):
    model = Detalle
    extra = 1
    classes = ('grp-collapse grp-open',)
    fields = ('code', 'name', 'cantidad', 'precio')


class factura_cabezera(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('numero', 'name', 'subtotal', 'descuento', 'iva', 'total')
    list_filter = ('cliente',)
    search_fields = ('name', 'identificacion', 'numero')
    fieldsets = (

        ('Datos Generales del Documento', {

                'classes': ('grp-collapse grp-open',),

                'fields': (
                            ('numero', 'fecha', 'usuario'),

                            ('code', 'name', 'identificacion'),

                            ('telefono', 'email'),

                            'direccion'
                            )
                            }),
                            )

    inlines = [factura_detalle]

admin.site.register(Factura, factura_cabezera)
