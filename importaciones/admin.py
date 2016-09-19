from django.contrib import admin
from .models import *


class importacion_admin(admin.ModelAdmin):
    list_display = ('nombre', )
    change_form_template = "admin/moneycash/modelo.html"

admin.site.register(Importacion, importacion_admin)
