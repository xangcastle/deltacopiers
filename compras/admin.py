from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import *


class factura_detalle(admin.TabularInline):
    form = DetalleForm
    model = Detalle
    extra = 0
    classes = ('grp-collapse grp-open box-detalle',)
    fields = ('code', 'name', 'cantidad', 'precio', 'descuento', 'iva',
            'producto_total')


class factura_cabezera(admin.ModelAdmin):
    form = FacturaForm
    date_hierarchy = 'fecha'
    list_display = ('numero', 'fecha', 'name', 'subtotal', 'descuento', 'iva',
        'total')
    list_filter = ('proveedor',)
    search_fields = ('name', 'identificacion', 'numero')
    fieldsets = (
        ('', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (
                            ('numero', 'fecha', 'code'),
                        )
        }),
        ('Datos del Proveedor', {
                'classes': ('box_cliente', ),
                'fields': (
                            ('name', 'identificacion'),
                            ('telefono', 'email'),
                            'direccion',
                        )
        }),
        ("Detalle de Productos", {"classes":
            ("placeholder detalle_set-group",), "fields": ()}),
        ('', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (
                            ('aplica_iva', 'aplica_ir', 'aplica_al'),
                        )
        }),
        ('Totales', {
                'classes': ('',),
                'fields': (('subtotal', 'descuento', 'iva'),
                            ('ir', 'al', 'total'),
                            )
                            }),
                            )

    inlines = [factura_detalle]

admin.site.register(Factura, factura_cabezera)


class proveedor_admin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'identificacion', 'email', 'telefono')
    search_fields = ('code', 'name', 'identificacion', 'email')

admin.site.register(Proveedor, proveedor_admin)


class producto_admin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'precio', 'costo')
    search_fields = ('code', 'name')

admin.site.register(Producto, producto_admin)
