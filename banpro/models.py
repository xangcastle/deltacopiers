from __future__ import unicode_literals

from django.db import models


class Puntos(models.Model):
    tipo = models.CharField(max_length=125, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    direccion = models.TextField(max_length=255, null=True, blank=True)
    nombre = models.CharField(max_length=125, null=True, blank=True)
    horario = models.CharField(max_length=125, null=True, blank=True)

    def __unicode__(self):
        return self.nombre
