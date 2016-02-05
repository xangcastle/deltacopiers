from django.db import models
from moneycash.entidad import Entidad
from moneycash.documento import Documento
from moneycash.produccion.models import Cliente, Area
from moneycash.models import Moneda
from datetime import timedelta


class factura_detalle(models.Model):
    factura = models.ForeignKey('Factura')
    item = models.ForeignKey('Item')
    cantidad = models.FloatField(default=1)
    precio = models.FloatField(default=0.0)
    descuento = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    area = models.ForeignKey(Area, null=True, blank=True)

    def top(self):
        top = 0
        for r in factura_detalle.objects.filter(
            factura=self.factura).order_by('id'):
                if r.id == self.id:
                    return 296 + (top * 24)
                top += 1

    def save(self, *args, **kwargs):
        self.total = round((self.cantidad * self.precio)
         - (self.cantidad * self.descuento), 2)
        self.factura.save()
        super(factura_detalle, self).save()

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'productos o servicios'


class Factura(Documento):
    TIPO_COMPRA = (('CO', 'CONTADO'), ('CR', 'CREDITO'))
    fecha_vence = models.DateField(null=True, blank=True,
        verbose_name="fecha de vencimiento",
        help_text="si se deja en blanco se aplica el plazo del provedor")
    comentarios = models.TextField(max_length=400, null=True, blank=True)
    cliente = models.ForeignKey(Cliente)
    tipo = models.CharField(max_length=2, default="CR",
        verbose_name="tipo de pago de la compra", choices=TIPO_COMPRA)
    moneda = models.ForeignKey(Moneda, default=1,
        related_name='produccion_factura_moneda')
    subtotal = models.FloatField(default=0.0)
    descuento = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)
    exento_iva = models.BooleanField(default=False)
    x_iva = models.FloatField(default=100, blank=True)
    ir = models.FloatField(default=0.0, verbose_name="retencion del ir")
    exento_ir = models.BooleanField(default=False)
    x_ir = models.FloatField(default=100, blank=True)
    al = models.FloatField(default=0.0, verbose_name="retencion de la alcaldia")
    exento_al = models.BooleanField(default=False,
        verbose_name="exento alcaldia")
    x_al = models.FloatField(default=100, blank=True)
    total = models.FloatField(default=0.0)
    abonado = models.FloatField(default=0.0)
    saldo = models.FloatField(default=0.0)
    tc = models.FloatField(null=True, default=0.0)

    def detalle(self):
        return factura_detalle.objects.filter(factura=self)

    def get_subtotal(self):
        monto = 0.0
        if self.detalle():
            for p in self.detalle():
                monto += (p.cantidad * p.precio)
        return round(monto, 2)

    def get_descuento(self):
        monto = 0.0
        if self.detalle():
            for p in self.detalle():
                monto += (p.cantidad * p.descuento)
        return round(monto, 2)

    def subtotal_descontado(self):
        monto = 0.0
        monto += (self.subtotal - self.descuento)
        return round(monto, 2)

    def get_ir(self):
        monto = 0.0
        if not self.exento_ir:
            if self.subtotal_descontado() >= 1000:
                monto += (self.subtotal_descontado() * 0.02)
        return round(monto, 2)

    def get_al(self):
        monto = 0.0
        if not self.exento_al:
            if self.subtotal_descontado() >= 1000:
                monto += (self.subtotal_descontado() * 0.01)
        return round(monto, 2)

    def get_iva(self):
        monto = 0.0
        if not self.exento_iva:
            monto += (self.subtotal_descontado() * 0.15)
        return round(monto, 2)

    def get_total(self):
        monto = 0.0
        monto += (self.subtotal - self.descuento) + self.iva
        return round(monto, 2)

    def get_saldo(self):
        if self.tipo == 'CO':
            self.abonado = self.total - (self.ir + self.al)
        monto = 0.0
        monto += (self.total - (self.ir + self.al + self.abonado))
        return round(monto, 2)

    def get_fecha_vence(self):
        if self.tipo == "CO":
            return None
        if self.tipo == "CR" and self.fecha_vence \
        and self.fecha_vence > self.fecha:
            return self.fecha_vence
        if self.tipo == "CR" and not self.fecha_vence:
            if self.cliente and self.cliente.plazo > 0:
                return self.fecha + timedelta(days=self.cliente.plazo)
            else:
                return self.fecha
        if self.fecha_vence and self.fecha > self.fecha_vence \
        and self.tipo == "CR":
            return self.fecha + timedelta(days=self.cliente.plazo)

    def calcular(self):
        self.subtotal = self.get_subtotal()
        self.descuento = self.get_descuento()
        self.ir = self.get_ir()
        self.al = self.get_al()
        self.iva = self.get_iva()
        self.total = self.get_total()
        self.saldo = self.get_saldo()
        self.fecha_vence = self.get_fecha_vence()

    def save(self, *args, **kwargs):
        self.calcular()
        super(Factura, self).save()

    def subtotal_cordobas(self):
        return round(self.subtotal * self.tc, 2)

    def iva_cordobas(self):
        return round(self.iva * self.tc, 2)

    def total_cordobas(self):
        return round(self.total * self.tc, 2)


class Item(Entidad):
    categoria = models.ForeignKey('Categoria')
    precio = models.FloatField(default=0.0)


class Categoria(Entidad):
    pass


