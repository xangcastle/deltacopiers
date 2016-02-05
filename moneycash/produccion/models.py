from django.db import models
from moneycash.entidad import Entidad, datos_generales
from moneycash.documento import Documento
from django.contrib.auth.models import User
from moneycash.models import Periodo as base_periodo, Moneda,\
Documento as comprobante, Movimiento, TipoDoc
from django.db.models import Sum
from datetime import timedelta
from moneycash.contabilidad.models import Cuenta


def activar_equipos(periodo):
    es = Equipo.objects.filter(activo=True)
    for e in es:
        n = equipo_periodo(periodo=periodo, equipo=e,
            contador_inicial=e.contador_actual,
            contador_final=e.contador_actual)
        n.save()


def crear_recibos(periodo):
    areas = Area.objects.filter(activo=True).values_list('id', flat=True)
    recibos = Recibo.objects.filter(periodo=periodo)
    if recibos:
        areas = list(set(areas) - set(recibos.values_list('area_id',
            flat=True)))
    for a in areas:
        area = Area.objects.get(id=a)
        r = Recibo(fecha=periodo.fin_produccion, area=area)
        r.save()
        for e in area.equipos.filter(activo=True):
            rd = recibo_detalle(recibo=r, equipo=e, precio=area.item.precio,
                fecha_inicial=periodo.inicio_produccion,
                fecha_final=periodo.fin_produccion)
            rd.save()


def cargar_copias(periodo):
    equipos = equipo_periodo.objects.filter(periodo=periodo)
    recibos = Recibo.objects.filter(periodo=periodo, impreso=False)
    for e in equipos:
        areas = recibo_detalle.objects.filter(equipo=e.equipo,
            recibo__in=recibos)
        total = areas.count()
        copias = 0
        if total > 0:
            copias = round(e.copias / total, 0)
        areas.update(copias=copias)
    for r in recibos:
        r.calcular()
        r.save()


def facturar(recibos):
    for r in recibos:
        f, created = Factura.objects.get_or_create(fecha=r.fecha,
        cliente=r.area.cliente, impreso=False)
        dd = factura_detalle(factura=f, item=r.area.item,
            precio=r.area.item.precio, cantidad=r.copias, area=r.area)
        dd.save()


def contabilizar_depreciacion(periodos):
    for p in periodos:
        d = comprobante()
        d.fecha = p.fin_produccion
        d.tipodoc = TipoDoc.objects.get(name='DEPRECIACION')
        d.name = 'Se Registra Comprobante por Depreciacion de Equipos del Periodo ' + str(p)
        d.save()
        for e in equipo_periodo.objects.filter(periodo=p):
            mi = Movimiento()
            mi.documento = d
            mi.cuenta = e.equipo.get_cuenta_inventario()
            mi.debe = (e.contador_final
            - e.contador_inicial) * e.equipo.depreciacion_copia
            mi.save()
            md = Movimiento()
            md.documento = d
            md.cuenta = e.equipo.get_cuenta_depreciacion()
            md.haber = (e.contador_final
            - e.contador_inicial) * e.equipo.depreciacion_copia
            md.save()


def cerrar(periodo):
        for r in periodo.equipos():
            e = Equipo.objects.get(id=r.equipo.id)
            e.contador_actual = r.contador_final
            e.depreciar()
            e.save()
        periodo.cerrado = True
        periodo.save()


class Periodo(base_periodo):
    class Meta:
        proxy = True

    def equipos(self):
        return equipo_periodo.objects.filter(periodo=self)

    def recibos(self):
        return Recibo.objects.filter(periodo=self)

    def copias_equipos(self):
        if self.equipos():
            return self.equipos().aggregate(Sum('copias'))['copias__sum']

    def copias_areas(self):
        if self.equipos():
            return self.recibos().aggregate(Sum('copias'))['copias__sum']

    def importe_produccion(self):
        if self.equipos():
            return self.recibos().aggregate(Sum('importe'))['importe__sum']


class equipo_periodo(models.Model):
    periodo = models.ForeignKey(Periodo)
    equipo = models.ForeignKey('Equipo')
    contador_inicial = models.PositiveIntegerField()
    contador_final = models.PositiveIntegerField()
    copias = models.PositiveIntegerField(null=True, blank=True, default=0)

    #def __unicode__(self):
        #return str(self.equipo) + str(self.total_copias)

    def get_copias(self):
        if self.contador_inicial and self.contador_final:
            return self.contador_final - self.contador_inicial
        else:
            return 0

    class Meta:
        verbose_name = 'equipo'
        verbose_name_plural = 'equipos en produccion'

    def save(self, *args, **kwargs):
        self.copias = self.get_copias()
        self.equipo.actualizar_contador(self.contador_final)
        super(equipo_periodo, self).save()


class recibo_detalle(models.Model):
    recibo = models.ForeignKey('Recibo')
    equipo = models.ForeignKey('Equipo')
    copias = models.FloatField(default=0.0)
    precio = models.FloatField(default=0.0)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()

    def __unicode__(self):
        return str(self.equipo) + ' copias: ' + str(self.copias)

    def importe(self):
        return round(self.copias * self.precio, 2)

    def dias_facturados(self):
        return int((self.fecha_final - self.fecha_inicial).days)

    def top(self):
        top = 0
        for r in recibo_detalle.objects.filter(
            recibo=self.recibo).order_by('equipo'):
                if r.id == self.id:
                    return 363 + (top * 20)
                top += 1

    class Meta:
        verbose_name = 'equipo'
        verbose_name_plural = 'detalle de copias por equipo'

    def save(self, *args, **kwargs):
        super(recibo_detalle, self).save()
        self.recibo.save()


class Recibo(Documento):
    area = models.ForeignKey('Area')
    copias = models.FloatField(default=0.0)
    importe = models.FloatField(default=0.0)
    tc = models.FloatField(default=0.0)

    def detalle(self):
        return recibo_detalle.objects.filter(recibo=self)

    def get_copias(self):
        copias = 0
        if self.detalle():
            copias += self.detalle().aggregate(Sum('copias'))['copias__sum']
        return copias

    def get_importe(self):
        monto = 0.0
        if self.detalle():
            for d in self.detalle():
                monto += d.importe()
        return round(monto, 2)

    def calcular(self):
        self.copias = self.get_copias()
        self.importe = self.get_importe()

    def str_numero(self):
        if self.numero:
            return str(self.numero).zfill(6)
        else:
            return '0'.zfill(6)

    def ultimos_seis(self):
        ps = Periodo.objects.filter(
            fecha_inicial__lte=self.periodo.fecha_inicial)[:10]
        rs = Recibo.objects.filter(periodo__in=ps,
            area=self.area).order_by('fecha')
        data = []
        for r in rs:
            d = {'periodo': str(r.periodo)[:3], 'copias': int(r.copias)}
            data.append(d)
        return data

    def save(self, *args, **kwargs):
        self.calcular()
        super(Recibo, self).save()


class Area(Entidad):
    cliente = models.ForeignKey('Cliente')
    ubicacion = models.ForeignKey('Ubicacion')
    encargado = models.CharField(max_length=100, default='')
    unidad_ejecutora = models.CharField(max_length=10, default='')
    equipos = models.ManyToManyField('Equipo',
        verbose_name='equipos que usa el area')
    item = models.ForeignKey('Item', null=True, blank=True,
        verbose_name='plan de facturarion')


class Ubicacion(Entidad):
    user = models.ForeignKey(User)
    direccion = models.TextField(max_length=250, null=True, blank=True)


class Cliente(Entidad, datos_generales):
    limite_credito = models.FloatField(null=True, blank=True, default=0,
        verbose_name="limite de credito")
    saldo = models.FloatField(default=0, blank=True,
        verbose_name="saldo inicial")
    plazo = models.PositiveIntegerField(default=0,
        help_text="plazo de credito expresado en cantidad de dias",
        null=True)
    contacto = models.CharField(max_length=75, null=True, blank=True)
    nombre_area = models.CharField(max_length=75, null=True, blank=True)

    def facturas(self):
        return Factura.objects.filter(cliente=self)


class Equipo(Entidad):
    marca = models.ForeignKey('Marca')
    modelo = models.CharField(max_length=30, default='')
    serie = models.CharField(max_length=30, default='')

    ubicacion = models.ForeignKey('Ubicacion', null=True, blank=True)
    velocidad = models.PositiveIntegerField(default=0,
        verbose_name='velocidad del equipo')
    precio_copia = models.FloatField(null=True, blank=True)
    costo_copia = models.FloatField(null=True, blank=True)

    contador_inicial = models.PositiveIntegerField(default=0,
        help_text='contador que tenia el equipo al momento de la compra')
    contador_actual = models.PositiveIntegerField(default=0)
    vida_util = models.PositiveIntegerField(default=1000000)
    costo_compra = models.FloatField(null=True, blank=True,
        verbose_name='costo de compra')
    depreciacion_copia = models.FloatField(null=True, blank=True,
        verbose_name='depreciacion por copia')
    valor_depreciado = models.FloatField(null=True, blank=True,
        verbose_name='total depreciado')
    precio_venta = models.FloatField(null=True, blank=True,
        verbose_name='valor en libros')

    def __unicode__(self):
        s = []
        if self.code:
            s.append(self.code)
        if self.modelo:
            s.append(self.modelo)
        if self.serie:
            s.append(self.serie)
        return ' - '.join(s)

    def actualizar_contador(self, c):
        if c > self.contador_actual:
            self.contador_actual = c

    def depreciar(self):
        if self.contador_inicial and self.contador_actual and self.vida_util \
            and self.costo_compra \
            and self.contador_actual > self.contador_inicial:
            self.depreciacion_copia = round(self.costo_compra / (
                self.vida_util - self.contador_inicial), 4)
            self.valor_depreciado = round(self.depreciacion_copia * (
                self.contador_actual - self.contador_inicial), 2)
            self.precio_venta = round(self.costo_compra
            - self.valor_depreciado, 2)

    def get_cuenta_inventario(self):
        c, created = Cuenta.objects.get_or_create(
            cuenta=Cuenta.objects.get(code='010201'),
            code='010201' + self.code, name=self.modelo + ' - '
            + self.serie, saldo=round(self.costo_compra * 25.3352, 2))
        return c

    def get_cuenta_depreciacion(self):
        c, created = Cuenta.objects.get_or_create(
            cuenta=Cuenta.objects.get(code='010205'),
            code='010205' + self.code, name=self.modelo + ' - '
            + self.serie)
        return c

    def save(self, *args, **kwargs):
        self.depreciar()
        super(Equipo, self).save()


class Marca(Entidad):
    pass


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


class Consumible(Entidad):
    costo = models.FloatField(null=True, blank=True)
    existencia = models.FloatField(null=True, blank=True)