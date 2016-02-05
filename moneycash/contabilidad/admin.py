from django.contrib import admin
from moneycash.admin import base_tabular
from import_export.admin import ImportExportModelAdmin
from .models import *


class cuenta_tabular(base_tabular):
    model = Cuenta
    fields = ('code', 'name', 'saldo', 'saldo_actual')
    readonly_fields = ('saldo', 'saldo_actual')


class cuenta_admin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'saldo', 'saldo_actual', 'activo',
        'naturaleza', 'grupo')
    list_filter = ('activo', 'naturaleza')
    fieldsets = (('Datos de la Cuenta', {'classes': ('grp-collapse grp-open',),
    'fields': (('name', 'code', 'activo'), ('cuenta', 'naturaleza'),
    ('saldo', 'saldo_actual'))
    }),)
    ordering = ('code',)
    readonly_fields = ('saldo', 'saldo_actual')
    search_fields = ('code', 'name')
    inlines = [cuenta_tabular]


class periodo_admin(admin.ModelAdmin):
    fields = (('fecha_inicial', 'fecha_final'), ('code', 'cerrado'))
    readonly_fields = ('code', 'cerrado')
    list_display = ('code', 'fecha_inicial', 'fecha_final', 'cerrado')
    actions = ['action_recalcular', 'action_cerrar']

    def action_recalcular(self, request, queryset):
        grupos = Cuenta().grupos()
        cuentas = Cuenta.objects.filter(id__in=grupos)
        balanza = Balanza.objects.filter(cuenta__in=cuentas)
        for b in balanza:
            b.actualizar_saldo()
    action_recalcular.short_description = \
    'recalcular saldos de los periodos seleccionados'

    def action_cerrar(self, request, queryset):
        for p in queryset:
            cerrar(p)
    action_cerrar.short_description = 'cerrar periodos seleccionados'


class comprobante_movimientos(base_tabular):
    raw_id_fields = ('cuenta', )
    autocomplete_lookup_fields = {
        'fk': ['cuenta', ],
        }
    model = Movimiento
    fields = ('cuenta', 'debe', 'haber')


class comprobante_admin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('code', 'fecha', 'concepto',
        'sucursal', 'sumas_iguales', 'diferencia')
    list_filter = ('periodo', 'user', 'sumas_iguales')
    search_fields = ('numero', 'code', 'concepto')

    fieldsets = (('Datos Generales', {'classes': ('grp-collapse grp-open',),
    'fields': (('numero', 'fecha'), 'concepto')}),
        ("Detalle Inlines", {"classes":
            ("placeholder movimiento_set-group",), "fields": ()}),
        ('Totales', {'classes': ('grp-collapse grp-open',),
            'fields': (('sumas_iguales', 'total_debe', 'total_haber',
            'diferencia'),)}))

    readonly_fields = ('sumas_iguales', 'total_debe', 'total_haber',
        'diferencia')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    inlines = [comprobante_movimientos]


class balanza_admin(admin.ModelAdmin):
    list_display = ('cuenta', 'saldo_inicial', 'saldo_final', 'periodo')
    list_filter = ('periodo',)
    search_fields = ('cuenta__code', 'cuenta__name')


admin.site.register(Periodo, periodo_admin)
admin.site.register(Cuenta, cuenta_admin)
admin.site.register(Comprobante, comprobante_admin)
admin.site.register(migracion, ImportExportModelAdmin)
admin.site.register(Balanza, balanza_admin)