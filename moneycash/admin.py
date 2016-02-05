from django.contrib import admin
from django.contrib.admin import site
from .models import *
from import_export.admin import ImportExportModelAdmin
import adminactions.actions as actions

actions.add_to_site(site)


class entidad_admin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'activo')
    list_filter = ('activo',)
    actions = ['activar', 'inactivar']
    ordering = ('code',)
    search_fields = ('code', 'name')
    ordering = ('name',)

    def inactivar(self, request, queryset):
        queryset.update(activo=False)
    inactivar.short_description = "Deactivate selected objects"

    def activar(self, request, queryset):
        queryset.update(activo=True)
    activar.short_description = "Activate selected objects"


class base_tabular(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    extra = 0


class kardex_tabular(base_tabular):
    model = Kardex
    fields = ('item', 'cantidad')


class movimiento_tabular(base_tabular):
    model = Movimiento


class base_documento_admin(ImportExportModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('numero', 'fecha', 'user', 'sucursal',
        'impreso', 'entregado', 'contabilizado')
    list_filter = ('tipodoc', 'periodo', 'user', 'sucursal', 'impreso',
        'entregado', 'contabilizado')
    search_fields = ('numero',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class documento_admin(base_documento_admin):
    inlines = [kardex_tabular, movimiento_tabular]


class documento_caja_admin(ImportExportModelAdmin):
    def save_model(self, request, obj, form, change):
        super(documento_admin, self).save_model()
        obj.cierre_caja = CierreCaja.objects.get(fecha_inicial__lte=self.fecha,
            fecha_final__gte=self.fecha)
        obj.save()


class periodo_admin(ImportExportModelAdmin):
    list_display = ('fecha_inicial', 'fecha_final', 'iva_contra', 'iva_pagado',
        'ir_cobrado', 'ir_pagado', 'al_recaudado', 'al_pagado', 'cerrado')


class factura_admin(documento_admin):
    fields = ('fecha', 'cliente_codigo', 'cliente_nombre', 'cliente_telefono',
    'cliente_direccion', 'cliente_ident')


class cuenta_admin(entidad_admin):
    list_display = ('code', 'name', 'saldo', 'activo')
    ordering = ('code',)


class tipodoc_admin(entidad_admin):
    list_display = ('code', 'name', 'afectacion', 'contabiliza', 'activo')
    list_filter = ('afectacion', 'contabiliza', 'activo')
    fields = (('code', 'name'), ('afectacion', 'contabiliza'), 'activo')


class total_periodo_admin(admin.ModelAdmin):
    list_display = ('periodo', 'iva_pagado', 'iva_contra', 'ir_cobrado',
        'ir_pagado', 'al_recaudado', 'al_pagado')


class item_admin(entidad_admin):
    list_filter = ('marca', 'categoria')
    list_display = ('code', 'name', 'marca', 'categoria', 'existencias')
    fieldsets = (('Datos Generales', {'classes': ('grp-collapse grp-open',),
    'fields': (('code', 'name'), ('marca', 'categoria'))}),
        ('Datos de Comercializacion', {'classes': ('grp-collapse grp-open',),
            'fields': (('precio', 'costo'), ('descuento', 'existencias'),
                'activo')}))


class relaciones_comerciales(base_tabular):
    model = relacion_comercial


class socio_comercial(entidad_admin):
    list_display = ('code', 'name', 'identificacion', 'telefono')
    inlines = [relaciones_comerciales]

admin.site.register(Periodo, periodo_admin)
admin.site.register(Sucursal, entidad_admin)
admin.site.register(Bodega, entidad_admin)
admin.site.register(Moneda, entidad_admin)
admin.site.register(Cuenta, cuenta_admin)
admin.site.register(TipoDoc, tipodoc_admin)
admin.site.register(SocioComercial, socio_comercial)


admin.site.register(Item, item_admin)
admin.site.register(Marca, entidad_admin)
admin.site.register(Categoria, entidad_admin)

admin.site.register(Documento, documento_admin)


class peb_admin(admin.ModelAdmin):
    list_display = ('item', 'bodega', 'existencias', 'ubicacion')

admin.site.register(Peb, peb_admin)


class tc_admin(ImportExportModelAdmin):
    list_display = ('fecha', 'oficial')
    list_filter = ('moneda',)
    date_hierarchy = 'fecha'


admin.site.register(Tc, tc_admin)