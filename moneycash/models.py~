# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Max
from datetime import datetime, timedelta
from .middlewares import get_current_user
from django.contrib.auth.models import User


class base(models.Model):

    def __iter__(self):
        for field_name in self._meta.get_all_field_names():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    class Meta:
        abstract = True


class datos_generales(base):
    identificacion = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="ruc/cedula")
    telefono = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


def get_code(entidad):
        model = type(entidad)
        code = ''
        sets = model.objects.all()
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
        return str(code).zfill(4)


class base_entidad(base):
    code = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="codigo")
    name = models.CharField(max_length=100, verbose_name="nombre")

    class Meta:
        abstract = True


class Entidad(base_entidad):
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.code and self.name:
            return str(self.code) + " " + self.name
        elif self.name:
            return self.name
        elif self.code:
            return str(self.code)
        else:
            return ''

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = get_code(self)
        super(Entidad, self).save()

    class Meta:
        abstract = True
        ordering = ['code']


class Moneda(Entidad):
    pass


class Tc(models.Model):
    fecha = models.DateField()
    oficial = models.FloatField()
    moneda = models.ForeignKey(Moneda, default=1)

    class Meta:
        verbose_name_plural = 'tasas de cambio'
        verbose_name = 'tasa de cambio'


class Periodo(base):
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    inicio_produccion = models.DateField(null=True, blank=True)
    fin_produccion = models.DateField(null=True, blank=True)
    inicio_ventas = models.DateField(null=True, blank=True)
    fin_ventas = models.DateField(null=True, blank=True)
    cerrado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.fecha_inicial.strftime("%B %Y")

    def short_name(self):
        return self.fecha_inicial.strftime("%B %Y")

    class Meta:
        ordering = ['-fecha_final']

    def totales(self):
        return total_periodo.objects.filter(periodo=self)

    def iva_pagado(self):
        if self.totales():
            return self.totales().aggregate(
                Sum('iva_pagado'))['iva_pagado__sum']
        else:
            return 0.0
    iva_pagado.short_description = 'iva a favor'

    def ir_cobrado(self):
        if self.totales():
            return self.totales().aggregate(
                Sum('ir_cobrado'))['ir_cobrado__sum']
        else:
            return 0.0

    def al_recaudado(self):
        if self.totales():
            return self.totales().aggregate(
                Sum('al_recaudado'))['al_recaudado__sum']
        else:
            return 0.0
    al_recaudado.short_description = 'AL en contra'

    def iva_contra(self):
        if self.totales():
            return self.totales().aggregate(
                Sum('iva_contra'))['iva_contra__sum']
        else:
            return 0.0
    iva_contra.short_description = 'iva en contra'

    def ir_pagado(self):
        if self.totales():
            return self.totales().aggregate(
                Sum('ir_pagado'))['ir_pagado__sum']
        else:
            return 0.0

    def al_pagado(self):
        if self.totales():
            return self.totales().aggregate(
                Sum('al_pagado'))['al_pagado__sum']
        else:
            return 0.0
    al_pagado.short_description = 'AL a favor'


class total_periodo(base):
    periodo = models.ForeignKey(Periodo)
    iva_pagado = models.FloatField(default=0)
    iva_contra = models.FloatField(default=0)
    ir_cobrado = models.FloatField(default=0)
    ir_pagado = models.FloatField(default=0)
    al_recaudado = models.FloatField(default=0)
    al_pagado = models.FloatField(default=0)

    class Meta:
        managed = False

    def save(self, *args, **kwargs):
        pass


class Sucursal(Entidad):
    class Meta:
        verbose_name_plural = 'sucursales'


class Bodega(Entidad):
    sucursal = models.ForeignKey(Sucursal)


class Cuenta(Entidad):
    '''
    Este es el modelo basico para crear el catalogo de cuentas contable
    '''

    cuenta = models.ForeignKey('self', related_name='cuenta_madre', null=True,
        blank=True)
    saldo = models.FloatField(default=0, help_text='saldo actual de la cuenta')

    def __unicode__(self, *args, **kwargs):
        return super(Cuenta, self).__unicode__(
            ) + ' Saldo: ' + str(self.saldo)

    def total_grupos(self):
        return Cuenta.objects.filter(cuenta=None).count()

    def sub_cuentas(self):
        return Cuenta.objects.filter(cuenta=self)

    def numero_sub_cuentas(self):
        return self.sub_cuentas().count()

    def get_code(self):
        if self.cuenta:
            if len(self.cuenta.code) >= 6:
                return self.cuenta.code + str(
                    self.cuenta.numero_sub_cuentas() + 1).zfill(4)
            else:
                return self.cuenta.code + str(
                    self.cuenta.numero_sub_cuentas() + 1).zfill(2)
        else:
            return str(self.total_grupos() + 1).zfill(2)

    def get_saldo(self):
        if self.sub_cuentas():
            return round(self.sub_cuentas().aggregate(
                Sum('saldo'))['saldo__sum'], 2)
        else:
            return self.saldo

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code()
        self.saldo = self.get_saldo()
        super(Cuenta, self).save()
        if self.cuenta:
            self.cuenta.saldo = self.cuenta.get_saldo()
            self.cuenta.save()

    def delete(self, *args, **kwargs):
        self.saldo = self.get_saldo()
        super(Cuenta, self).delete()

    class Meta:
        ordering = ['code']


class cuenta_periodo(base):
    periodo = models.ForeignKey(Periodo)
    cuenta = models.ForeignKey(Cuenta)
    saldo_inicial = models.FloatField(default=0)
    saldo_final = models.FloatField(default=0)


class Movimiento(base):
    documento = models.ForeignKey('Documento')
    cuenta = models.ForeignKey(Cuenta)
    debe = models.FloatField(default=0)
    haber = models.FloatField(default=0)

    def __unicode__(self):
        texto = []
        if self.debe > 0:
            texto.append('debitar ' + str(self.debe))
        if self.haber > 0:
            texto.append('acreditar ' + str(self.haber))
        return ' y '.join(texto)


class TipoDoc(Entidad):
    tipos_de_afectacion = ((1, 'POSITIVA'), (-1, 'NEGATIVA'),
        (0, 'SIN AFECTACION'))
    contabiliza = models.BooleanField(default=True,
        help_text='indica si el documento tiene afectacion contable')
    afectacion = models.IntegerField(choices=tipos_de_afectacion,
        help_text='tipo de afectacion inventarial')

    class Meta:
        verbose_name = 'tipo de documento'
        verbose_name_plural = 'tipos de documentos'


class Numeracion(base):
    tipodoc = models.ForeignKey(TipoDoc)
    sucursal = models.ForeignKey(Sucursal)
    numero_inicial = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('tipodoc', 'sucursal')


def get_numeracion(tipodoc, sucursal):
    return Numeracion.objects.get(tipodoc=tipodoc, sucursal=sucursal)


class datos_documento(base):
    fecha = models.DateTimeField(null=True, blank=True)
    fecha_vence = models.DateField(null=True, blank=True,
        verbose_name="fecha de vencimiento",
        help_text="si se deja en blanco se aplica el plazo del provedor")
    numero = models.PositiveIntegerField(null=True, blank=True)
    tipodoc = models.ForeignKey(TipoDoc, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_tipodoc")
    periodo = models.ForeignKey(Periodo, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_periodo")
    user = models.ForeignKey(User, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_user")
    sucursal = models.ForeignKey(Sucursal, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_sucursal")
    bodega = models.ForeignKey(Sucursal, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_bodega")
    moneda = models.ForeignKey(Moneda, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_moneda")
    autorizado = models.BooleanField(default=True)
    impreso = models.BooleanField(default=False)
    contabilizado = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    FORMAS_PAGO = (('CO', 'CONTADO'), ('CR', 'CREDITO'))
    forma_pago = models.CharField(max_length=2, default="CO",
        verbose_name="forma de pago", choices=FORMAS_PAGO)
    proveedor = models.ForeignKey('SocioComercial', null=True, blank=True,
        related_name='%(app_label)s_%(class)s_proveedor')
    cliente = models.ForeignKey('SocioComercial', null=True, blank=True,
        related_name='%(app_label)s_%(class)s_cliente')

    def __unicode__(self):
        if self.numero:
            return type(self).__name__ + " " + str(self.numero)
        else:
            return type(self).__name__

    class Meta:
        ordering = ['-numero']
        abstract = True

    def get_fecha_inicial(self, fecha):
        return datetime(fecha.year, fecha.month, 0o1)

    def get_fecha_final(self, fecha):
        if fecha.month == 12:
            return datetime(fecha.year + 1, 0o1, 0o1) - timedelta(days=1)
        else:
            return datetime(fecha.year,
                fecha.month + 1, 0o1) - timedelta(days=1)

    def get_periodo(self, fecha):
        p, created = Periodo.objects.get_or_create(
            fecha_inicial=self.get_fecha_inicial(fecha),
            fecha_final=self.get_fecha_final(fecha))
        return p

    def get_numero(self):
        return 0

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = datetime.now()
        self.periodo = self.get_periodo(self.fecha)
        if not self.numero:
            self.numero = self.get_numero()
        try:
            if not self.user:
                self.user = get_current_user()
        except:
            self.user = User.objects.all().order_by('id')[0]
        super(datos_documento, self).save()


class datos_cliente(base_entidad, datos_generales):
    class Meta:
        abstract = True


class datos_factura(base):
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
    tc = models.FloatField(null=True, default=1.0)

    class Meta:
        abstract = True

    def detalle(self):
        return Kardex.objects.filter(documento=self)

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

    def calcular_factura(self):
        self.subtotal = self.get_subtotal()
        self.descuento = self.get_descuento()
        self.ir = self.get_ir()
        self.al = self.get_al()
        self.iva = self.get_iva()
        self.total = self.get_total()
        self.saldo = self.get_saldo()


class base_documento(datos_documento, datos_cliente, datos_factura):
    class Meta:
        abstract = True


class Documento(base_documento):
    pass


class Kardex(base):
    documento = models.ForeignKey(Documento, null=True, blank=True)
    item = models.ForeignKey('Item')
    bodega = models.ForeignKey(Bodega, null=True, blank=True)
    ubicacion = models.CharField(max_length=10, null=True, blank=True)
    cantidad = models.FloatField(default=1)
    existencias = models.FloatField(default=0)
    saldo = models.FloatField(default=0)
    precio = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    costo_entrada = models.FloatField(default=0)
    costo_anterior = models.FloatField(default=0)
    costo_promedio = models.FloatField(default=0)
    costo_importacion = models.FloatField(default=0)
    costo_internacion = models.FloatField(default=0)
    recibido = models.FloatField(null=True, blank=True)


class Item(Entidad):
    marca = models.ForeignKey('Marca', null=True, blank=True)
    categoria = models.ForeignKey('Categoria', null=True, blank=True)
    existencias = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    precio = models.FloatField(default=0)
    costo = models.FloatField(default=0)
    comprar = models.BooleanField(default=True)
    vender = models.BooleanField(default=True)
    almacenar = models.BooleanField(default=True)
    factor = models.FloatField(default=2)


class Marca(Entidad):
    pass


class Categoria(Entidad):
    parent = models.ForeignKey('self', null=True, blank=True)


class base_sc(Entidad, datos_generales):
    class Meta:
        abstract = True


class SocioComercial(base_sc):
    class Meta:
        verbose_name_plural = 'socios comerciales'


class base_relacion_comercial(base):
    socio = models.ForeignKey(SocioComercial)
    RELACIONES = (
      ('CL', 'CLIENTE'),
      ('PR', 'PROVEEDOR'),
    )
    tipo_relacion = models.CharField(max_length=2,
        choices=RELACIONES, default='CL',
        verbose_name='tipo de relacion')
    tiempo_entrega = models.PositiveIntegerField(
        help_text="tiempo de entrega en dias para la mercaderia",
        verbose_name="tiempo de entrega", default=0, null=True)
    limite_credito = models.FloatField(null=True, blank=True, default=0,
        verbose_name="limite de credito")
    saldo = models.FloatField(default=0, blank=True,
        verbose_name="saldo inicial")
    plazo = models.PositiveIntegerField(default=0,
        help_text="plazo de credito expresado en cantidad de dias",
        null=True)

    class Meta:
        abstract = True


class relacion_comercial(base_relacion_comercial):
    class Meta:
        verbose_name = 'relacion comercial'
        verbose_name_plural = 'relaciones comerciales'


def update_cliente(cliente, datos):
    if datos['nombre'] is not None:
        cliente.name = datos['nombre']
    if datos['identificacion'] is not None:
        cliente.identificacion = datos['identificacion']
    if datos['telefono'] is not None:
        cliente.telefono = datos['telefono']
    if datos['direccion'] is not None:
        cliente.direccion = datos['direccion']
    cliente.save()


def get_cliente(nombre, identificacion, telefono, direccion):
    c = None
    d = {}
    d['nombre'] = nombre
    d['identificacion'] = identificacion
    d['telefono'] = telefono
    d['direccion'] = direccion
    if identificacion == '' or identificacion is None:
        if nombre == '' or nombre is None:
            return c
        else:
            c, created = SocioComercial.objects.get_or_create(name=nombre)
            update_cliente(c, d)
    else:
        c, created = SocioComercial.objects.get_or_create(
            identificacion=identificacion)
        update_cliente(c, d)
    return c


class socio(base_sc, base_relacion_comercial):
    def save(self, *args, **kwargs):
        sc = get_cliente(self.name, self.identificacion,
            self.telefono, self.direccion)

        rl, created = relacion_comercial.objects.get_or_create(socio=sc,
            tipo_relacion=self.tipo_relacion)
        rl.tiempo_entrega = self.tiempo_entrega
        rl.limite_credito = self.limite_credito
        rl.saldo = self.saldo
        rl.plazo = self.plazo
        rl.save()

    class Meta:
        abstract = True


class Peb(base):
    item = models.ForeignKey(Item, blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    existencias = models.FloatField(blank=True, null=True)
    ubicacion = models.CharField(max_length=10, blank=True)

    class Meta:
        managed = False


class cliente_manager(models.Manager):
    def get_queryset(self):
        return super(cliente_manager, self).get_queryset(
            ).filter(tipo_relacion='CL')


class proveedor_manager(models.Manager):
    def get_queryset(self):
        return super(proveedor_manager, self).get_queryset(
            ).filter(tipo_relacion='PR')


class Cliente(socio):
    objects = models.Manager()
    objects = cliente_manager()

    class Meta:
        managed = False
        db_table = 'prueba_cliente'

    def save(self, *args, **kwargs):
        self.tipo_relacion = 'CL'
        super(Cliente, self).save()


class Proveedor(socio):
    objects = models.Manager()
    objects = proveedor_manager()

    class Meta:
        managed = False
        db_table = 'prueba_cliente'

    def save(self, *args, **kwargs):
        self.tipo_relacion = 'PR'
        super(Proveedor, self).save()


def get_by_code(entidad, code):
    model = entidad.__class__
    return model.objects.get(code=code)


def get_by_number(tipodoc, number):
    return Documento.objects.get(tipodoc=tipodoc,
        numero=number)


def importar_compras(compras):
    for c in compras:
        d = Documento()
        d.fecha = c.fecha
        d.tipodoc = TipoDoc.objects.get(name='COMPRA')
        d.fecha_vence = c.fecha_vence
        d.user = c.user
        d.periodo = c.periodo
        d.numero = c.numero
        d.proveedor = get_by_code(SocioComercial(), c.proveedor.code)
        d.moneda = c.moneda
        d.subtotal = c.subtotal
        d.iva = c.iva
        d.ir = c.ir
        d.al = c.al
        d.total = c.total
        d.exento_al = c.exento_al
        d.exento_ir = c.exento_ir
        d.exento_iva = c.exento_iva
        d.saldo = c.saldo
        d.abonado = c.abonado
        d.forma_pago = c.tipo
        d.save()

        for cd in c.detalle():
            dd = Kardex()
            dd.documento = d
            dd.item = get_by_code(Item(), cd.producto.code)
            dd.cantidad = cd.cantidad
            dd.precio = cd.precio
            dd.descuento = cd.descuento
            dd.save()


def importar_ventas(ventas):
    for c in ventas:
        d = Documento()
        d.fecha = c.fecha
        d.tipodoc = TipoDoc.objects.get(name='VENTA')
        d.fecha_vence = c.fecha_vence
        d.user = c.user
        d.periodo = c.periodo
        d.numero = c.numero
        d.proveedor = get_by_code(SocioComercial(), c.cliente.code)
        d.moneda = c.moneda
        d.subtotal = c.subtotal
        d.iva = c.iva
        d.ir = c.ir
        d.al = c.al
        d.total = c.total
        d.exento_al = c.exento_al
        d.exento_ir = c.exento_ir
        d.exento_iva = c.exento_iva
        d.saldo = c.saldo
        d.abonado = c.abonado
        d.forma_pago = c.tipo
        d.save()

        for cd in c.detalle():
            dd = Kardex()
            dd.documento = d
            dd.item = get_by_code(Item(), cd.item.code)
            dd.cantidad = cd.cantidad
            dd.precio = cd.precio
            dd.descuento = cd.descuento
            dd.save()


def inicializar_saldos(periodos):
    cuentas = Cuenta.objects.filter(activo=True)
    for p in periodos:
        for c in cuentas:
            cp, created = cuenta_periodo.objects.get_or_create(periodo=p,
                cuenta=c)
            cp.saldo_inicial = c.saldo
            cp.save()

def aperturar(periodos):
    pass