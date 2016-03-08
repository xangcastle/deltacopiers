from django.contrib import admin
from .models import *
from .forms import *


class factura_detalle(admin.TabularInline):
    form = DetalleForm
    model = Detalle
    extra = 1
    classes = ('grp-collapse grp-open',)
    fields = ('code', 'name', 'cantidad', 'precio', 'descuento', 'iva',
            'total')


class factura_cabezera(admin.ModelAdmin):
    form = FacturaForm
    date_hierarchy = 'fecha'
    list_display = ('numero', 'name', 'subtotal', 'descuento', 'iva', 'total')
    list_filter = ('cliente',)
    search_fields = ('name', 'identificacion', 'numero')
    fieldsets = (
        ('', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (
                            ('numero', 'fecha', 'code'),
                        )
        }),
        ('Datos del Cliente', {
                'classes': ('box_cliente', ),
                'fields': (
                            ('name', 'identificacion'),
                            ('telefono', 'email'),
                            'direccion',
                        )
        }),
        ("Detalle de Productos", {"classes":
            ("placeholder detalle_set-group",), "fields": ()}),
        ('Totales', {
                'classes': ('',),
                'fields': (('subtotal', 'descuento', 'iva'),
                            ('aplica_iva', 'aplica_ir', 'aplica_al'),
                            ('ir', 'al', 'total'),
                            )
                            }),
                            )

    inlines = [factura_detalle]

admin.site.register(Factura, factura_cabezera)


class cliente_admin(admin.ModelAdmin):
    list_display = ('code', 'name', 'identificacion', 'email', 'telefono')
    search_fields = ('code', 'name', 'identificacion', 'email')

admin.site.register(Cliente, cliente_admin)


class producto_admin(admin.ModelAdmin):
    list_display = ('code', 'name', 'precio', 'costo')
    search_fields = ('code', 'name')

admin.site.register(Producto, producto_admin)
