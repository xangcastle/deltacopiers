from django.contrib import admin
from .models import Puntos
from import_export.admin import ImportExportModelAdmin


class puntos_admin(ImportExportModelAdmin):
    list_display = ('nombre', 'direccion', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


admin.site.register(Puntos, puntos_admin)