"""
Administrador con permisos para consulta(view)

Es una clase que extiende de admin.ModelAdmin y se utilizar para integrar
el admin con permiso de consulta.

Hay que integrarlo con el script que agrega a todos los modelos el permiso
de consulta(view):
https://gist.github.com/nicpottier/880901

Por Ejemplo si tenemos dos modelos "Poll" y "Choice" (Ejemplos del tutorial
de Django) agregamos lo siquiente en "admin.py" de la app:

from django.contrib import admin
from polls.models import Choice, Poll
# Script para agregar los nuevas clases
from adminview import *

class ChoiceInline(ViewAdminStackedInline):
    model = Choice
    extra = 3

class PollAdmin(ViewAdmin):
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)

El archivo se debe colocar en el path de python.
"""
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


class ViewAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        ct = ContentType.objects.get_for_model(self.model)
        salida = False
        if request.user.is_superuser:
            salida = True
        else:
            if request.user.has_perm('%s.view_%s' % (ct.app_label, ct.model)):
                salida = True
            else:
                if request.user.has_perm('%s.change_%s' %
                    (ct.app_label, ct.model)):
                    salida = True
                else:
                    salida = False
        return salida

    def get_readonly_fields(self, request, obj=None):
        ct = ContentType.objects.get_for_model(self.model)
        if not request.user.is_superuser and \
            request.user.has_perm('%s.view_%s' % (ct.app_label, ct.model)):

            return list(self.readonly_fields) + \
              [el.name for el in self.model._meta.fields]
        else:
            return self.readonly_fields


class ViewAdminTabularInline(admin.TabularInline):
    def has_change_permission(self, request, obj=None):
        ct = ContentType.objects.get_for_model(self.model)
        salida = False
        if request.user.is_superuser:
            salida = True
        else:
            if request.user.has_perm('%s.view_%s' % (ct.app_label, ct.model)):
                salida = True
            else:
                if request.user.has_perm('%s.change_%s'
                    % (ct.app_label, ct.model)):
                    salida = True
                else:
                    salida = False
        return salida

    def get_readonly_fields(self, request, obj=None):
        ct = ContentType.objects.get_for_model(self.model)
        if not request.user.is_superuser and \
            request.user.has_perm('%s.view_%s' % (ct.app_label, ct.model)):

            return list(self.readonly_fields) + \
                [el.name for el in self.model._meta.fields]
        else:
            return self.readonly_fields


class ViewAdminStackedInline(admin.StackedInline):
    def has_change_permission(self, request, obj=None):
        ct = ContentType.objects.get_for_model(self.model)
        salida = False
        if request.user.is_superuser:
            salida = True
        else:
            if request.user.has_perm('%s.view_%s' % (ct.app_label, ct.model)):
                salida = True
            else:
                if request.user.has_perm('%s.change_%s' %
                    (ct.app_label, ct.model)):
                    salida = True
                else:
                    salida = False
        return salida

    def get_readonly_fields(self, request, obj=None):
        ct = ContentType.objects.get_for_model(self.model)
        if not request.user.is_superuser and \
            request.user.has_perm('%s.view_%s' % (ct.app_label, ct.model)):
            return list(self.readonly_fields) + \
                [el.name for el in self.model._meta.fields]
        else:
            return self.readonly_fields
