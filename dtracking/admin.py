from django.contrib import admin
from base.admin import entidad_admin
from grappelli.forms import GrappelliSortableHiddenMixin
from django.contrib.admin import widgets
from django import forms
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from .models import *



class detalle_tabular(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = DetalleGestion
    extra = 0
    fields = ('nombreVariable', 'tipo', 'titulo', 'habilitado', 'requerido',
    'orden')
    sortable_field_name = 'orden'


class tipoGestion_admin(entidad_admin):
    inlines = [detalle_tabular, ]


class gestion_admin(admin.ModelAdmin):
    list_display = ('destinatario', 'direccion', 'departamento', 'municipio',
    'barrio', 'tipo_gestion', 'user', 'realizada', 'fecha')
    list_filter = ('departamento', 'municipio', 'zona', 'realizada')
    search_fields = ('destinatario', 'departamento__name',
    'municipio__name', 'barrio__name', 'zona__name')


class elemento_admin(admin.ModelAdmin):
    list_display = ('valor', 'combo')
    list_filter = ('combo',)


class barrio_admin(entidad_admin):
    list_display = ('code', 'name', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('code', 'name', 'municipio__name',
    'municipio__departamento__name')


class gestor_admin(admin.ModelAdmin):
    list_display = ('user', 'numero', 'image_thumb')


class import_admin(entidad_admin):
    list_display = ('destinatario', 'direccion', 'telefono', 'barrio',
    'municipio', 'departamento')

    actions = ['action_integrar']

    class integrationForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        fecha_asignacion = forms.DateField(
            widget=widgets.AdminDateWidget())
        fecha_vencimiento = forms.DateField(
            widget=widgets.AdminDateWidget())
        tipo_gestion = forms.ModelChoiceField(
            queryset=TipoGestion.objects.all().order_by('name'))
        eliminar = forms.BooleanField(required=False,
        help_text="eliminar registros despues de integrarlos")

    def action_integrar(self, request, queryset):
        message = ""
        form = None
        msj = integrar(queryset)
        if 'apply' in request.POST:
            form = self.integrationForm(request.POST)
            if form.is_valid():
                for c in queryset:
                    c.integrar_registro(form.cleaned_data['fecha_asignacion'],
                    form.cleaned_data['fecha_vencimiento'],
                    form.cleaned_data['tipo_gestion'],
                    form.cleaned_data['eliminar'])
                self.message_user(request, msj)
                return HttpResponseRedirect(
                    "/admin/dtracking/import")

        if not form:
            form = self.integrationForm(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})
        data = {'queryset': queryset, 'form': form,
            'header_tittle': 'Por Favor complete todos los campos',
            'explanation':
                'Los siguientes registros seran procesados:',
                'action': 'action_integrar'}
        data.update(csrf(request))
        self.message_user(request, message)
        return render_to_response('admin/base_action.html', data)

admin.site.register(Gestion, gestion_admin)
admin.site.register(TipoGestion, tipoGestion_admin)
admin.site.register(Departamento, entidad_admin)
admin.site.register(Municipio, entidad_admin)
admin.site.register(Barrio, barrio_admin)
admin.site.register(Zona, entidad_admin)
admin.site.register(Elemento, elemento_admin)
admin.site.register(Gestor, gestor_admin)
admin.site.register(Import, import_admin)
