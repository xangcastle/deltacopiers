from django.contrib import admin
from .models import *


class factura_detalle(admin.TabularInline):
    model = Detalle
    extra = 0
    classes = ('grp-collapse grp-open',)
    fields = ('code', 'name', 'cantidad', 'precio')


class factura_admin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('numero', 'name', )
    list_filter = ('cliente',)
    search_fields = ('name', 'identificacion', 'numero')

    inlines = [factura_detalle]

admin.site.register(Factura, factura_admin)
