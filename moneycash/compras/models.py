from django.db import models
#from moneycash.entidad import Entidad
#from moneycash.documento import Documento
from moneycash.models import Documento as base_documento,\
Kardex as base_detalle, TipoDoc, Proveedor as base_proveedor
#from django.db.models import Sum
#from datetime import timedelta
#from moneycash.models import Documento as doc, Kardex as det


#class Producto(Entidad):
    #marca = models.ForeignKey('Marca', null=True, blank=True)
    #categoria = models.ForeignKey('Categoria', null=True, blank=True)
    #existencias = models.FloatField(default=0)
    #descuento = models.FloatField(default=0)
    #precio = models.FloatField(default=0)
    #costo = models.FloatField(default=0)


#class Marca(Entidad):
    #pass


#class Categoria(Entidad):
    #parent = models.ForeignKey('self', null=True, blank=True)


#class Proveedor(datos_generales, Entidad):
    #TIPO_OPTIONS = (
      #('LO', 'NACIONAL'),
      #('EX', 'EXTRAJERO'),
    #)
    #tipo = models.CharField(max_length=2, choices=TIPO_OPTIONS, default='LO')
    #tiempo_entrega = models.PositiveIntegerField(
        #help_text="tiempo de entrega en dias para la mercaderia",
        #verbose_name="tiempo de entrega", default=0, null=True)
    #limite_credito = models.FloatField(null=True, blank=True, default=0,
        #verbose_name="limite de credito")
    #saldo = models.FloatField(default=0, blank=True,
        #verbose_name="saldo inicial")
    #plazo = models.PositiveIntegerField(default=0,
        #help_text="plazo de credito expresado en cantidad de dias",
        #null=True)

    #def compras(self):
        #return Compra.objects.filter(proveedor=self)

    #def compras_credito_cordobas(self):
        #return self.compras().filter(tipo="CR", moneda=1)

    #def compras_credito_dolares(self):
        #return self.compras().filter(tipo="CR", moneda=2)

    #def total_compras(self):
        #if self.compras():
            #return round(self.compras().aggregate(Sum('total'))['total__sum'],
                 #2)
        #else:
            #return 0

    #def get_saldo(self):
        #saldo = []
        #if self.compras_credito_cordobas():
            #cordobas = str(round(self.compras_credito_cordobas().aggregate(
                #Sum('saldo'))['saldo__sum'], 2)) + " Cordobas"
            #saldo.append(cordobas)
        #if self.compras_credito_dolares():
            #dolares = str(round(self.compras_credito_dolares().aggregate(
                #Sum('saldo'))['saldo__sum'], 2)) + " Dolares"
            #saldo.append(dolares)
        #if len(saldo) > 0:
            #return " y ".join(saldo)
        #else:
            #return 0

    #get_saldo.short_description = "saldo"

    #get_saldo.allow_tags = True

    #class Meta:
        #verbose_name_plural = "proveedores"


#class Compra(Documento):
    #TIPO_COMPRA = (('CO', 'CONTADO'), ('CR', 'CREDITO'))
    #fecha_vence = models.DateField(null=True, blank=True,
        #verbose_name="fecha de vencimiento",
        #help_text="si se deja en blanco se aplica el plazo del provedor")
    #comentarios = models.TextField(max_length=400, null=True, blank=True)
    #proveedor = models.ForeignKey(Proveedor)
    #tipo = models.CharField(max_length=2, default="CR",
        #verbose_name="tipo de pago de la compra", choices=TIPO_COMPRA)
    #moneda = models.ForeignKey(Moneda, default=1)
    #subtotal = models.FloatField(default=0.0)
    #descuento = models.FloatField(default=0.0)
    #iva = models.FloatField(default=0.0)
    #exento_iva = models.BooleanField(default=False)
    #x_iva = models.FloatField(default=100, blank=True)
    #ir = models.FloatField(default=0.0, verbose_name="retencion del ir")
    #exento_ir = models.BooleanField(default=False)
    #x_ir = models.FloatField(default=100, blank=True)
    #al = models.FloatField(default=0.0, verbose_name="retencion de la alcaldia")
    #exento_al = models.BooleanField(default=False,
        #verbose_name="exento alcaldia")
    #x_al = models.FloatField(default=100, blank=True)
    #total = models.FloatField(default=0.0)
    #abonado = models.FloatField(default=0.0)
    #saldo = models.FloatField(default=0.0)

    #def detalle(self):
        #return compra_detalle.objects.filter(compra=self)

    #def get_subtotal(self):
        #monto = 0.0
        #if self.detalle():
            #for p in self.detalle():
                #monto += (p.cantidad * p.precio)
        #return round(monto, 2)

    #def get_descuento(self):
        #monto = 0.0
        #if self.detalle():
            #for p in self.detalle():
                #monto += (p.cantidad * p.descuento)
        #return round(monto, 2)

    #def subtotal_descontado(self):
        #monto = 0.0
        #monto += (self.subtotal - self.descuento)
        #return round(monto, 2)

    #def get_ir(self):
        #monto = 0.0
        #if not self.exento_ir:
            #if self.subtotal_descontado() >= 1000:
                #monto += (self.subtotal_descontado() * 0.02)
        #return round(monto, 2)

    #def get_al(self):
        #monto = 0.0
        #if not self.exento_al:
            #if self.subtotal_descontado() >= 1000:
                #monto += (self.subtotal_descontado() * 0.01)
        #return round(monto, 2)

    #def get_iva(self):
        #monto = 0.0
        #if not self.exento_iva:
            #monto += (self.subtotal_descontado() * 0.15)
        #return round(monto, 2)

    #def get_total(self):
        #monto = 0.0
        #monto += (self.subtotal - self.descuento) + self.iva
        #return round(monto, 2)

    #def get_saldo(self):
        #if self.tipo == 'CO':
            #self.abonado = self.total - (self.ir + self.al)
        #monto = 0.0
        #monto += (self.total - (self.ir + self.al + self.abonado))
        #return round(monto, 2)

    #def get_fecha_vence(self):
        #if self.tipo == "CO":
            #return None
        #if self.tipo == "CR" and self.fecha_vence \
        #and self.fecha_vence > self.fecha:
            #return self.fecha_vence
        #if self.tipo == "CR" and not self.fecha_vence:
            #if self.proveedor and self.proveedor.plazo > 0:
                #return self.fecha + timedelta(days=self.proveedor.plazo)
            #else:
                #return self.fecha
        #if self.fecha_vence and self.fecha > self.fecha_vence \
        #and self.tipo == "CR":
            #return self.fecha + timedelta(days=self.proveedor.plazo)

    #def calcular(self):
        #self.subtotal = self.get_subtotal()
        #self.descuento = self.get_descuento()
        #self.ir = self.get_ir()
        #self.al = self.get_al()
        #self.iva = self.get_iva()
        #self.total = self.get_total()
        #self.saldo = self.get_saldo()
        #self.fecha_vence = self.get_fecha_vence()

    #def save(self, *args, **kwargs):
        #self.calcular()
        #super(Compra, self).save()

    #class Meta:
        #unique_together = ("proveedor", "numero")
        #verbose_name = "factura"


#class compra_detalle(models.Model):
    #compra = models.ForeignKey(Compra, null=True, blank=True)
    #producto = models.ForeignKey(Producto)
    #cantidad = models.FloatField(default=1)
    #existencias = models.FloatField(default=0)
    #saldo = models.FloatField(default=0)
    #precio = models.FloatField(default=0)
    #descuento = models.FloatField(default=0)
    #costo_entrada = models.FloatField(default=0)
    #costo_promedio = models.FloatField(default=0)
    #costo_importacion = models.FloatField(default=0)
    #costo_internacion = models.FloatField(default=0)
    #recibido = models.FloatField(null=True, blank=True)

    #def __unicode__(self):
        #return '%s %s' % (str(self.cantidad), str(self.producto))

    #def save(self, *args, **kwargs):
        #super(compra_detalle, self).save()
        #self.compra.save()

    #class Meta:
        #verbose_name = "producto"
        #verbose_name_plural = 'detalle de la compra'


class Kardex(base_detalle):
    class Meta:
        proxy = True


class compra_manager(models.Manager):
    def get_queryset(self):
        return super(compra_manager, self).get_queryset(
            ).filter(tipodoc=TipoDoc.objects.get(name='COMPRA'))


class Documento(base_documento):
    objects = models.Manager()
    objects = compra_manager()

    class Meta:
        proxy = True
        verbose_name = 'compra'


class Proveedor(base_proveedor):
    class Meta:
        proxy = True
        verbose_name_plural = 'proveedores'