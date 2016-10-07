from django.contrib import admin
from .models import *


class importacion_admin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('nombre', 'estado')
    change_form_template = "admin/moneycash/modelo.html"
    list_filter = ('estado', )

admin.site.register(Importacion, importacion_admin)
