from django.contrib import admin
from .models import *
from django.contrib.admin import site
import adminactions.actions as actions
actions.add_to_site(site)


class productor_tabular(admin.TabularInline):
    model = productor
    extra = 0


class detalle_tabular(admin.TabularInline):
    exclude = ('dia_8', 'precio')
    model = detalle
    extra = 0


class productor_admin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'precio_pago', 'linea')
    list_filter = ('linea',)
    search_fields = ('nombre', 'cedula')


class linea_admin(admin.ModelAdmin):
    list_display = ('nombre', 'recolector', 'precio', 'lista_productores')
    inlines = [productor_tabular]


def cerrar_periodo(modeladmin, request, queryset):
    queryset.update(cerrado=True)
cerrar_periodo.short_description = "Cerrar los periodos selecionados"


class periodo_admin(admin.ModelAdmin):
    list_display = ('fecha_inicial', 'fecha_final', 'cerrado',
        'resumen_recoleccion', 'resumen_pago')
    list_filter = ('cerrado',)
    actions = [cerrar_periodo]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not obj.cerrado:
            lineas = linea.objects.all()
            for l in lineas:
                if not recoleccion.objects.filter(periodo=obj, linea=l):
                    r = recoleccion()
                    r.linea = l
                    r.periodo = obj
                    r.save()
                    for p in r.linea.productores():
                        d = detalle()
                        d.recoleccion = r
                        d.productor = p
                        d.precio = p.precio_pago()
                        d.save()
        else:
            recs = recoleccion.objects.filter(periodo=obj)
            for r in recs:
                for p in r.detalles():
                    p.precio = p.productor.precio_pago()
                    p.save()
        obj.save()


class recoleccion_admin(admin.ModelAdmin):
    change_list_template = "lacteos/recolecion_admin.html"
    list_display = ('linea', 'periodo', 'cerrado', 'imprimir',
        'retenciones', 'detalle_linea')
    inlines = [detalle_tabular]

    def get_queryset(self, request):
        periodos = periodo.objects.filter(cerrado=False)
        return recoleccion.objects.filter(periodo__in=periodos)


class adelanto_admin(admin.ModelAdmin):
    list_display = ('productor', 'monto', 'tipo', 'comentario')
    list_filter = ('tipo',)
    search_fields = ('productor', 'monto')

    def get_queryset(self, request):
        periodos = periodo.objects.filter(cerrado=False)
        return adelanto.objects.filter(periodo__in=periodos)


class cliente_admin(admin.ModelAdmin):
    list_display = ('nombre', 'ident')


class entrega_admin(admin.ModelAdmin):
    list_display = ('cliente', 'cantidad')
    exclude = ('periodo',)


admin.site.register(productor, productor_admin)
admin.site.register(linea, linea_admin)
admin.site.register(periodo, periodo_admin)
admin.site.register(recoleccion, recoleccion_admin)
admin.site.register(cliente, cliente_admin)
admin.site.register(adelanto, adelanto_admin)
admin.site.register(entrega, entrega_admin)
