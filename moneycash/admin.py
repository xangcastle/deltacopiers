from django.contrib import admin
from .models import *
from base.admin import entidad_admin


class cliente_admin(entidad_admin):
    list_display = ('code', 'name', 'ident', 'phone', 'email', 'address')
    search_fields = ('code', 'name', 'ident', 'email')

admin.site.register(Cliente, cliente_admin)


class producto_admin(entidad_admin):
    list_display = ('code', 'name', 'no_part', 'price', 'cost',
    'existencia_total')
    search_fields = ('code', 'name', 'no_part')

admin.site.register(Producto, producto_admin)

admin.site.register(Sucursal, entidad_admin)
admin.site.register(Bodega, entidad_admin)
admin.site.register(TipoPago, entidad_admin)


class existencia_admin(admin.ModelAdmin):
    list_display = ('bodega', 'producto', 'cantidad')
    search_fields = ('producto__code', 'producto__name', 'bodega__name')
admin.site.register(Existencia, existencia_admin)


class detalle_factura(admin.TabularInline):
    model = Detalle
    fields = ('producto', 'bodega', 'cantidad', 'price', 'discount', 'cost')
    extra = 0


class factura_admin(admin.ModelAdmin):
    inlines = [detalle_factura]
    list_display = ('numero', 'cliente', 'subtotal', 'descuento', 'iva',
    'retension', 'total')


admin.site.register(Factura, factura_admin)
