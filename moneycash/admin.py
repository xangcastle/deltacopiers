from django.contrib import admin
from .models import *
from base.admin import entidad_admin
from django import forms
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.admin import site
import adminactions.actions as actions
actions.add_to_site(site)

class cliente_admin(entidad_admin):
    list_display = ('code', 'name', 'ident', 'phone', 'email', 'address', 'tipo')
    search_fields = ('code', 'name', 'ident', 'email')
    list_filter = ('tipo',)

admin.site.register(Cliente, cliente_admin)


admin.site.register(Categoria)
admin.site.register(CuentaBanco)


class producto_admin(entidad_admin):
    change_form_template = "admin/moneycash/producto.html"
    list_display = ('code', 'name', 'no_part', 'price', 'cost', 'categoria',
    'existencia_total', 'details', 'vender', 'comprar', 'almacenar', 'image_thumb')
    search_fields = ('code', 'name', 'no_part')
    list_filter = ('categoria', 'vender', 'comprar', 'almacenar')
    fieldsets = (
        ('Datos Generales', {
            'fields': ('name', ('code', 'short_name'),
                      ('categoria', 'price', 'cost'), ('imagen', 'no_part'),
                      ('vender', 'comprar', 'almacenar'),
                      'details')
        }),
    )

    class factorForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        factor = forms.FloatField(required=True,label= "Factor a Aplicar", widget=forms.NumberInput(attrs={'placeholder': 'Factor a Aplicar'}))


    actions = ['aplicar_factor']

    def aplicar_factor(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.factorForm(request.POST)
            if form.is_valid():
                factor = float(form.cleaned_data['factor'])
                for q in queryset:
                    q.price = round((q.cost * factor), 2)
                    q.save()
                return HttpResponseRedirect(
                    "/admin/moneycash/producto")

        if not form:
            form = self.factorForm(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})
        data = {'queryset': queryset, 'form': form,
                'header_tittle': 'Indique el Factor de Comercializacion que le aplicara a los productos selecionados.',
                'explanation': 'El precio de los siguientes productos se vera afectado:',
                'action': 'aplicar_factor'}
        data.update(csrf(request))
        return render_to_response('admin/moneycash/action.html', data)
    aplicar_factor.short_description = "Aplicar factor a los productos selecionado/s"


admin.site.register(Producto, producto_admin)
admin.site.register(Sucursal, entidad_admin)
admin.site.register(Bodega, entidad_admin)
admin.site.register(Banco, entidad_admin)
admin.site.register(Roc)


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
    'ir', 'al', 'total')


admin.site.register(Factura, factura_admin)


class preventa_detalle(admin.TabularInline):
    model = Orden
    extra = 0

class preventa_admin(admin.ModelAdmin):
    list_display = ('fecha', 'cliente')
    inlines = [preventa_detalle, ]

admin.site.register(Preventa, preventa_admin)

class sms_admin(entidad_admin):
    list_display = ('numero', 'texto', 'enviado')
    search_fields = ('numero', 'texto')
    list_filter = ('enviado', 'numero')

admin.site.register(SMS, sms_admin)

class codigos_error(admin.TabularInline):
    model = Codigo
    extra = 0
    fields = ('tipo', 'codigo', 'short_description', 'details')

class modelo_admin(admin.ModelAdmin):
    change_form_template = "admin/moneycash/modelo.html"
    list_display = ('serie', 'modelo')
    list_filter = ('serie',)
    inlines = [codigos_error,]


admin.site.register(Modelo, modelo_admin)

class tc_admin(entidad_admin):
    date_hierarchy = 'fecha'
    list_display = ('fecha', 'oficial', 'compra', 'venta')
    ordering = ('fecha',)
    actions = []
admin.site.register(TC, tc_admin)


class cuenta_admin(entidad_admin):
    list_display = ('codigo', 'nombre', 'operativa', 'tipo', 'prueba')
    list_filter = ('tipo', 'operativa')
    search_fields = ('codigo', 'nombre')
    ordering = ('codigo',)
admin.site.register(Cuenta, cuenta_admin)
