from __future__ import unicode_literals

from django.db import models
from django.db.models import Max, Sum
from django.conf import settings

User = settings.AUTH_USER_MODEL


def get_code(entidad, length=4):
        model = type(entidad)
        code = ''
        sets = model.objects.filter(code__isnull=False)
        if sets:
            maxi = str(sets.aggregate(Max('code'))['code__max'])
            if maxi:
                consecutivo = list(range(1, int(maxi)))
                ocupados = list(sets.values_list('code',
                flat=True))
                n = 0
                for l in ocupados:
                    ocupados[n] = int(str(l))
                    n += 1
                disponibles = list(set(consecutivo) - set(ocupados))
                if len(disponibles) > 0:
                    code = min(disponibles)
                else:
                    code = max(ocupados) + 1
        else:
            code = 1
        return str(code).zfill(length)


class base_proveedor(models.Model):
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    identificacion = models.CharField(max_length=14, null=True, blank=True,
        help_text="RUC/CEDULA")
    telefono = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=165, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)

    def estadisticas(self):
        return 0.25

    class Meta:
        abstract = True


class Factura(base_proveedor):

    """
    Modelo factura. Cabezera de Documento
    """

    proveedor = models.ForeignKey('Proveedor', null=True)
    #datos del documento
    numero = models.CharField(max_length=25, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, null=True,
        related_name="compras_factura_user")

    #totales del documento
    subtotal = models.FloatField(null=True, blank=True)
    descuento = models.FloatField(null=True, blank=True)
    iva = models.FloatField(null=True, blank=True)
    ir = models.FloatField(null=True, blank=True)
    al = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    aplica_iva = models.BooleanField(default=True)
    aplica_ir = models.BooleanField(default=False)
    aplica_al = models.BooleanField(default=False)

    def get_numero(self):
        queryset = Factura.objects.all().order_by('numero')
        if queryset and queryset.count() > 0:
            return int(queryset.aggregate(Max('numero'))['numero__max']) + 1
        else:
            return 1

    def detalle(self):
        return Detalle.objects.filter(factura=self)

    def get_subtotal(self):
        if not self.detalle():
            return 0.0
        else:
            return None

    def get_cliente(self):
        c, created = Proveedor.objects.get_or_create(
            identificacion=self.identificacion)
        c.name = self.name
        c.telefono = self.telefono
        c.direccion = self.direccion
        c.email = self.email
        c.save()
        return c

    def save(self, *args, **kwargs):
        if not self.cliente:
            self.cliente = self.get_cliente()
        if not self.numero:
            self.numero = self.get_numero()
        if not self.subtotal:
            self.subtotal = self.get_subtotal()
        super(Factura, self).save()

    def __unicode__(self):
        return 'Factura #' + str(self.numero)


class Detalle(models.Model):
    factura = models.ForeignKey(Factura)
    producto = models.ForeignKey('Producto', null=True)
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    cantidad = models.FloatField(null=True)
    precio = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    iva = models.FloatField(null=True)

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Proveedor(base_proveedor):

    def facturas(self):
        return Factura.objects.filter(cliente=self)

    @property
    def venta_total(self):
        if self.facturas():
            return self.facturas().aggregate(Sum('subtotal'))['subtotal__sum']

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)

    def __iter__(self):
        for field_name in self._meta.get_all_field_names():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    def __getitem__(self, fieldname):
        try:
            return getattr(self, fieldname)
        except:
            return None

    def get_code(self):
        return get_code(self)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code()
        super(Proveedor, self).save()


class Producto(models.Model):
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    precio = models.FloatField(null=True)
    costo = models.FloatField(null=True)

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)

    def __getitem__(self, fieldname):
        try:
            return getattr(self, fieldname)
        except:
            return None
