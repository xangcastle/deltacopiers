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
    list_display = ('code', 'name', 'ident', 'phone', 'email', 'address')
    search_fields = ('code', 'name', 'ident', 'email')

admin.site.register(Cliente, cliente_admin)


admin.site.register(Categoria)


class producto_admin(entidad_admin):
    list_display = ('code', 'name', 'no_part', 'price', 'cost', 'categoria',
    'existencia_total', 'details', 'image_thumb')
    search_fields = ('code', 'name', 'no_part')
    list_filter = ('categoria',)

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


class salidaDetalle_admin(admin.TabularInline):
    model = salidaDetalle
    extra = 0
    raw_id_fields = ('producto',)
    autocomplete_lookup_fields = {
        'fk': ['producto',],
        }


class salida_admin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('numero', 'concepto', 'user_solicita')
    inlines = [salidaDetalle_admin]
    fields = ('numero', 'concepto')

admin.site.register(Salida, salida_admin)


class preventa_detalle(admin.TabularInline):
    model = Orden
    extra = 0

class preventa_admin(admin.ModelAdmin):
    list_display = ('fecha', 'cliente')
    inlines = [preventa_detalle, ]

admin.site.register(Preventa, preventa_admin)

admin.site.register(SMS)
