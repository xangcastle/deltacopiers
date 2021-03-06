from __future__ import unicode_literals

from django.db import models


def porcentaje(num, per):
    return round((num * per) / 100, 2)


class Pais(models.Model):
    nombre = models.CharField(max_length=65)
    zona = models.ForeignKey('Zona')

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "paises"


class Zona(models.Model):
    nombre = models.CharField(max_length=65)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Tarifa(models.Model):
    zona = models.ForeignKey(Zona)
    peso = models.FloatField(default=0.5, verbose_name="peso en kilogramos")
    precio = models.FloatField(default=0.0)

    class Meta:
        ordering = ['zona', 'precio']


class Cliente(models.Model):
    contacto = models.CharField(max_length=220)
    cargo = models.CharField(max_length=220)
    empresa = models.CharField(max_length=220)
    email = models.EmailField(max_length=220)
    telefono = models.CharField(max_length=220)

    def __unicode__(self):
      return "%s - %s" % (self.contacto, self.empresa)

class Importacion(models.Model):
    cliente = models.ForeignKey(Cliente, null=True)
    fecha = models.DateField(null=True)
    fecha_vence = models.DateField(null=True)
    numero = models.PositiveIntegerField(null=True)
    nombre = models.CharField(max_length=165, unique=True)
    blog = models.TextField(max_length=99999)
    proforma = models.FileField(null=True, blank=True)
    proforma_proveedor = models.FileField(null=True, blank=True, verbose_name="proforma del proveedor")
    orden = models.FileField(null=True, blank=True, verbose_name="orden de compra")
    plist = models.FileField(null=True, blank=True, verbose_name="packing list")
    estado = models.CharField(max_length=100, null=True, blank=True)
    peso = models.FloatField(null=True, default=0.0)
    pais = models.ForeignKey(Pais, verbose_name="pais de origen", null=True)
    flete = models.FloatField(null=True, default=0.0,
        verbose_name="air cargo/flete")
    aduanas = models.FloatField(null=True, default=0.0)
    divisa = models.FloatField(null=True, default=0.0)
    banco = models.FloatField(null=True, default=0.0)

    tsi = models.FloatField(null=True, default=0.5, verbose_name="TSI")
    spe = models.FloatField(null=True, default=5.0, verbose_name="SPE")
    ssa = models.FloatField(null=True, default=0.0, verbose_name="SSA")
    almacen = models.FloatField(null=True, default=0.0)
    transporte = models.FloatField(null=True, default=0.0)

    otros = models.FloatField(null=True, default=0.0)

    factor = models.FloatField(null=True, default=2.0)
    utilidad = models.FloatField(null=True, default=0.0)
    guia = models.CharField(max_length=25, null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def items(self):
        return Item.objects.filter(orden=self)

    def total_fob(self):
        t = 0.0
        for i in self.items():
            t += (i.cantidad * i.fob)
        return t

    def sub_total(self):
        t = 0.0
        for i in self.items():
            t += (i.cantidad * i.precio)
        return round(t, 2)

    def iva(self):
        iva = 0.0
        for i in self.items():
            iva += (porcentaje(i.cip, i.iva) * i.cantidad)
        return round(iva, 2)

    def total(self):
        return self.sub_total() + self.iva()

    def to_json(self):
        obj =  {
          'nombre': self.nombre,
          'numero': str(self.numero).zfill(6) ,
          'contacto': self.cliente.contacto,
          'empresa': self.cliente.empresa,
          'cargo': self.cliente.cargo,
          'telefono': self.cliente.telefono,
          'fecha': str(self.fecha),
          'fecha_vence': str(self.fecha_vence),
          'subtotal': str(self.sub_total()),
          'iva': str(self.iva()),
          'total': str(self.total())
          }
        obj['detalle'] = [x.to_json() for x in self.items()]
        return obj

    def get_numero(self):
        try:
            return Importacion.objects.all().order_by('-numero')[0].numero + 1
        except:
            return 1

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.get_numero()
        super(Importacion, self).save()

    class Meta:
        verbose_name_plural = "importaciones"


class Item(models.Model):
    orden = models.ForeignKey(Importacion)
    cantidad = models.FloatField()
    descripcion = models.CharField(max_length=300)
    fob = models.FloatField(null=True, default=0.0)
    cip = models.FloatField(null=True, default=0.0)
    cif = models.FloatField(null=True, default=0.0)
    dai = models.PositiveIntegerField(null=True, default=0, verbose_name="% DAI")
    isc = models.PositiveIntegerField(null=True, default=0, verbose_name="% ISC")
    iva = models.PositiveIntegerField(null=True, default=15, verbose_name="% IVA")
    precio = models.FloatField(null=True, default=0.0)
    anexo = models.FileField(null=True, blank=True)

    @property
    def total(self):
        return self.cantidad * self.precio

    def to_json(self):
        return {
          'cantidad': str(self.cantidad),
          'descripcion': self.descripcion,
          'precio': str(self.precio),
          'total': str(self.total),
        }
