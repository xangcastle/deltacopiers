from __future__ import unicode_literals

from django.db import models


class Importacion(models.Model):
    fecha = models.DateField(null=True)
    nombre = models.CharField(max_length=165)
    blog = models.TextField(max_length=99999)
    proforma = models.FileField(null=True, blank=True)
    proforma_proveedor = models.FileField(null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
