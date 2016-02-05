from django.contrib import admin
from .models import *
from moneycash.entidad import entidad_admin
from moneycash.documento import documento_admin
from django.template.context import RequestContext
from django.shortcuts import render_to_response


class contadores_tabular(admin.TabularInline):
    model = equipo_periodo
    extra = 0
    classes = ('grp-collapse grp-open',)
    #fields = ('equipo', 'contador_inicial', 'contador_final')


class detalle_recibo_tabular(admin.TabularInline):
    model = recibo_detalle
    extra = 0
    classes = ('grp-collapse grp-open',)


class recibo_admin(documento_admin):
    list_display = ('numero', 'fecha', 'area', 'copias', 'importe')
    inlines = [detalle_recibo_tabular]
    fieldsets = (('Datos del Recibo',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('numero', 'fecha'), 'area'), }),
            ("Detalle Inlines", {"classes":
            ("placeholder recibo_detalle_set-group",), "fields": ()}),
                ('Datos de Facturacion',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('copias', 'importe', 'tc'),), }),)
    actions = ['generar_imprimir', 'facturar']
    list_filter = ('periodo', 'area')

    def generar_imprimir(self, request, queryset):
        for r in queryset:
            r.impreso = True
            r.save()
        id_unico = False
        if queryset.count() == 1:
            id_unico = True
        ctx = {'queryset': queryset, 'id_unico': id_unico}
        return render_to_response('moneycash/produccion/recibo.html', ctx,
            context_instance=RequestContext(request))
    generar_imprimir.short_description = "Imprimir recibos selecionados"

    def facturar(self, request, queryset):
        facturar(queryset)


class periodo_admin(admin.ModelAdmin):
    list_display = ('short_name', 'inicio_produccion', 'fin_produccion',
    'copias_equipos', 'copias_areas', 'importe_produccion', 'cerrado')
    inlines = [contadores_tabular]
    fieldsets = (('Datos del Periodo', {'classes': ('grp-collapse grp-open',),
        'fields': (('fecha_inicial', 'fecha_final'),
            ('inicio_produccion', 'fin_produccion'),)}),)

    def generar_recibos(self, request, queryset):
        for p in queryset:
            crear_recibos(p)

    generar_recibos.short_description = \
    'generar recibos de los periodos seleccionados'

    def cargar_copias(self, request, queryset):
        for p in queryset:
            cargar_copias(p)

    cargar_copias.short_description = \
    'cargar copias de los periodos seleccionados'

    def activar_equipos(self, request, queryset):
        for p in queryset:
            activar_equipos(p)

    activar_equipos.short_description = \
    'activar equipos de los periodos seleccionados'

    def cerrar_(self, request, queryset):
        for p in queryset:
            cerrar(p)

    cerrar.short_description = \
    'cerrar periodos seleccionados'

    actions = [generar_recibos, cargar_copias, activar_equipos, cerrar_]


class equipo_admin(entidad_admin):
    list_display = ('code', 'modelo', 'serie', 'marca', 'contador_inicial',
        'contador_actual', 'vida_util', 'costo_compra', 'depreciacion_copia',
        'valor_depreciado', 'precio_venta', 'activo',)
    search_fields = ('code', 'name', 'modelo', 'serie')
    list_filter = ('activo', 'marca', 'ubicacion')
    fieldsets = (('Datos Generales',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('code', 'modelo'), ('serie', 'marca'),
                ('velocidad', 'ubicacion')), }),
                ('Datos de Facturacion',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('contador_inicial', 'contador_actual', 'vida_util'),
                ('costo_compra', 'depreciacion_copia', 'valor_depreciado'),
                ('precio_venta', 'activo'), ('costo_copia',
                    'precio_copia')), }),)
    ordering = ['code']


class cliente_admin(entidad_admin):
    list_display = ('code', 'name', 'identificacion', 'telefono', 'direccion',
        'activo')
    search_fields = ('code', 'name', 'telefono')
    list_filter = ('activo', )
    fieldsets = (('Datos Generales',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('code', 'name'), ('identificacion', 'telefono'),
                ('direccion',), ('contacto', 'nombre_area'), 'activo'), }),)


class area_admin(entidad_admin):
    list_display = ('code', 'name', 'encargado', 'unidad_ejecutora',
        'ubicacion', 'activo')
    search_fields = ('code', 'name', 'encargado')
    list_filter = ('activo', 'cliente', 'ubicacion')
    fieldsets = (('Datos del Area',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('code', 'name'), ('encargado', 'unidad_ejecutora'),
                ('equipos', 'activo'), ('ubicacion', 'cliente'), 'item'), }),)


class factura_detalle_admin(admin.TabularInline):
    model = factura_detalle
    extra = 0
    classes = ('grp-collapse grp-open',)


class factura_admin(documento_admin):
    list_display = ('numero', 'fecha', 'cliente', 'subtotal', 'descuento',
        'iva', 'total', 'total', 'tc', 'ir', 'al', 'impreso')

    fieldsets = (
            ('Datos de la Factura',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('numero', 'fecha'), 'cliente',
            ('exento_iva', 'exento_ir', 'exento_al')), }),

            ("Detalle Inlines",
            {"classes": ("placeholder factura_detalle_set-group",),
            'fields': ()}),

            ('Totales de la Factura',
            {'classes': ('grp-collapse grp-open',),
            'fields': (('subtotal', 'descuento'),
            ('iva', 'total'), ('ir', 'al'), 'tc'), }),
                )
    inlines = [factura_detalle_admin]

    actions = ['generar_imprimir']

    def generar_imprimir(self, request, queryset):
        id_unico = False
        if queryset.count() == 1:
            id_unico = True
        ctx = {'queryset': queryset, 'id_unico': id_unico}
        queryset.update(impreso=True)
        return render_to_response('moneycash/produccion/factura.html', ctx,
            context_instance=RequestContext(request))
    generar_imprimir.short_description = "Imprimir Facturas Selecionadas"


admin.site.register(Marca, entidad_admin)
admin.site.register(Equipo, equipo_admin)
admin.site.register(Area, area_admin)
admin.site.register(Ubicacion, entidad_admin)
admin.site.register(Cliente, cliente_admin)
admin.site.register(Periodo, periodo_admin)
admin.site.register(Recibo, recibo_admin)
admin.site.register(Factura, factura_admin)
admin.site.register(Item, entidad_admin)
admin.site.register(Categoria, entidad_admin)

