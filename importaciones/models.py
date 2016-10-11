from __future__ import unicode_literals

from django.db import models


class Importacion(models.Model):
    change_form_template = "/admin/importacion.html"
    fecha = models.DateField(null=True)
    nombre = models.CharField(max_length=165)
    blog = models.TextField(max_length=99999)
    proforma = models.FileField(null=True, blank=True)
    proforma_proveedor = models.FileField(null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    flete = models.FloatField(null=True, default=0.0,
        verbose_name="air cargo/flete")
    aduanas = models.FloatField(null=True, default=0.0)
    divisa = models.FloatField(null=True, default=0.0)
    banco = models.FloatField(null=True, default=0.0)

    def __unicode__(self):
        return self.nombre

    def items(self):
        return Item.objects.filter(orden=self)

    def total_fob(self):
        t = 0.0
        for i in self.items():
            t += (i.cantidad * i.fob)
        return t


class Item(models.Model):
    orden = models.ForeignKey(Importacion)
    cantidad = models.FloatField()
    descripcion = models.CharField(max_length=300)
    fob = models.FloatField(null=True, default=0.0)
    cip = models.FloatField(null=True, default=0.0)
    cif = models.FloatField(null=True, default=0.0)
    precio = models.FloatField(null=True, default=0.0)
    anexo = models.FileField(null=True, blank=True)
