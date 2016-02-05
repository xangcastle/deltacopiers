from django.db import models
from django.db.models import Sum, Max
from moneycash.models import base, Entidad
from django.contrib.auth.models import User
from datetime import datetime, timedelta


def get_code_periodo(fecha):
    return fecha.year * 12 + fecha.month


class Periodo(base):
    code = models.PositiveIntegerField(null=True, blank=True)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    cerrado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.fecha_inicial.strftime("%B %Y")

    def comprobantes(self):
        return Comprobante.objects.filter(periodo=self)

    def movimientos(self):
        return Movimiento.objects.filter(periodo=self)

    def balanza(self):
        return Balanza.objects.filter(periodo=self)

    def save(self, *args, **kwargs):
        self.code = get_code_periodo(self.fecha_inicial)
        super(Periodo, self).save()
        if not self.cerrado:
            aperturar(self)

    def delete(self, *args, **kwargs):
        for b in self.balanza():
            b.retroceder_saldo()
        super(Periodo, self).save()

    class Meta:
        ordering = ['-fecha_final']


class Cuenta(Entidad):
    cuenta = models.ForeignKey('self', related_name='cuenta_madre', null=True,
        blank=True)
    saldo = models.FloatField(default=0,
        verbose_name='saldo inicial')
    saldo_actual = models.FloatField(default=0)

    TIPOS_CUENTA = (
        ('AC', 'ACREDEDORA'),
        ('DE', 'DEUDORA'),
        )

    naturaleza = models.CharField(max_length=2, choices=TIPOS_CUENTA,
        blank=True)

    @property
    def grupo(self):
        return len(self.code)

    def __unicode__(self, *args, **kwargs):
        return super(Cuenta, self).__unicode__(
            ) + ' Saldo: ' + str(self.saldo_actual)

    def grupos(self):
        return Cuenta.objects.filter(cuenta=None)

    def total_grupos(self):
        return self.grupos.count()

    def sub_cuentas(self):
        return Cuenta.objects.filter(cuenta=self)

    def is_parent(self):
        if self.sub_cuentas():
            return True
        else:
            return False

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

    def get_cuenta(self):
        c = None
        code = ''
        if len(self.code) == 4:
            code = self.code[0:2]

        if len(self.code) == 6:
            code = self.code[0:4]

        if len(self.code) == 10:
            code = self.code[0:6]
        try:
            c = Cuenta.objects.get(code=code)
        except:
            pass
        return c

    def get_cuenta_mayor(self):
        try:
            return Cuenta.objects.get(code=self.code[0:4])
        except:
            return None

    def get_saldo(self):
        if self.sub_cuentas():
            return round(self.sub_cuentas().aggregate(
                Sum('saldo'))['saldo__sum'], 2)
        else:
            return self.saldo

    def get_saldo_actual(self):
        if self.sub_cuentas():
            return round(self.sub_cuentas().aggregate(
                Sum('saldo_actual'))['saldo_actual__sum'], 2)
        else:
            try:
                return Balanza.objects.get(cuenta=self,
                periodo=Periodo.objects.filter(
                    cerrado=False).order_by('fecha_inicial')[0]).saldo_final
            except:
                return 0

    def actualizar_saldo(self):
        if self.saldo != self.get_saldo():
            self.saldo = self.get_saldo()
            self.save()
        if self.saldo_actual != self.get_saldo_actual():
            self.saldo_actual = self.get_saldo_actual()
            self.save()

    def get_activo(self):
        if self.is_parent():
            return False
        if not self.is_parent() and self.saldo > 0:
            return True
        if not self.is_parent():
            return self.activo

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code()
        if not self.naturaleza and self.cuenta:
            self.naturaleza = self.cuenta.naturaleza
        if not self.naturaleza and not self.cuenta:
            self.naturaleza = 'DE'
        self.activo = self.get_activo()
        if not self.cuenta:
            self.cuenta = self.get_cuenta()
        super(Cuenta, self).save()
        if self.cuenta:
            c = Cuenta.objects.get(id=self.cuenta.id)
            c.actualizar_saldo()
        if self.is_parent():
            if self.saldo_actual != self.get_saldo():
                self.actualizar_saldo()

    def delete(self, *args, **kwargs):
        cuenta = None
        if self.cuenta:
            cuenta = Cuenta.objects.get(id=self.cuenta.id)
        super(Cuenta, self).delete()
        try:
            cuenta.actualizar_saldo()
        except:
            pass

    class Meta:
        ordering = ['code']
        verbose_name_plural = "catalogo de cuentas"


def cambiar_naturaleza(cuentas, naturaleza):
    for c in cuentas:
        c.naturaleza = naturaleza
        c.save()


class operativa_manager(models.Manager):
    def get_queryset(self):
        return super(operativa_manager, self).get_queryset().filter(activo=True)


class Operativa(Cuenta):
    objects = models.Manager()
    objects = operativa_manager()

    class Meta:
        proxy = True


class Balanza(base):
    periodo = models.ForeignKey(Periodo)
    cuenta = models.ForeignKey(Cuenta)
    saldo_inicial = models.FloatField(default=0)
    saldo_final = models.FloatField(default=0)

    class Meta:
        verbose_name = 'cuenta'
        verbose_name_plural = 'balanza de comprobacion'
        ordering = ['cuenta']

    def __unicode__(self):
        return 'Cuenta: %s | saldo inicial: %s | saldo final: %s' \
        % (self.cuenta.code, self.saldo_inicial, self.saldo_final)

    def sub_cuentas(self):
        return Balanza.objects.filter(periodo=self.periodo,
            cuenta__in=self.cuenta.sub_cuentas())

    def get_saldo_inicial(self):
        if self.cuenta.is_parent():
            return self.sub_cuentas().aggregate(
                Sum('saldo_inicial'))['saldo_inicial__sum']
        else:
            return self.saldo_inicial

    def movientos(self):
        return Movimiento.objects.filter(cuenta=self.cuenta,
            periodo=self.periodo)

    def credito(self):
        if self.movientos():
            return self.movientos().aggregate(Sum('haber'))['haber__sum']
        else:
            return 0

    def debito(self):
        if self.movientos():
            return self.movientos().aggregate(Sum('debe'))['debe__sum']
        else:
            return 0

    def get_saldo_final_by_movimientos(self):
        if self.cuenta.naturaleza == 'AC':
            return self.saldo_inicial + self.credito() - self.debito()
        if self.cuenta.naturaleza == 'DE':
            return self.saldo_inicial + self.debito() - self.credito()

    def get_saldo_final(self):
        if self.sub_cuentas():
            for c in self.sub_cuentas():
                c.actualizar_saldo()
            return self.sub_cuentas().aggregate(
                Sum('saldo_final'))['saldo_final__sum']
        else:
            return self.get_saldo_final_by_movimientos()

    def actualizar_saldo(self):
        if self.saldo_final != self.get_saldo_final():
            self.saldo_final = self.get_saldo_final()
            self.save()
        c = Cuenta.objects.get(id=self.cuenta.id)
        c.actualizar_saldo()
        c.save()

    def trasladar_saldo(self):
        c = Cuenta.objects.get(id=self.cuenta.id)
        c.saldo = self.saldo_final
        c.saldo_actual = self.saldo_final
        c.save()

    def retroceder_saldo(self):
        c = Cuenta.objects.get(id=self.cuenta.id)
        c.saldo = self.saldo_inicial
        c.saldo_actual = self.saldo_final
        c.save()

    def save(self, *args, **kwargs):
        #self.actualizar_saldo()
        super(Balanza, self).save()


def aperturar(periodo):
    cuentas_periodo = Cuenta.objects.filter(id__in=
    Balanza.objects.filter(periodo=periodo).values_list('cuenta',
            flat=True))
    cuentas_activas = Cuenta.objects.all()

    nuevas = cuentas_activas.exclude(id__in=cuentas_periodo).order_by('code')

    for c in nuevas:
        n = Balanza(periodo=periodo, cuenta=c, saldo_inicial=c.saldo,
            saldo_final=c.saldo)
        n.save()


def cerrar(periodo):
    for b in periodo.balanza():
        b.trasladar_saldo()
    periodo.cerrado = True
    periodo.save()


class Movimiento(base):
    comprobante = models.ForeignKey('Comprobante')
    cuenta = models.ForeignKey(Cuenta)
    periodo = models.ForeignKey(Periodo)
    debe = models.FloatField(default=0)
    haber = models.FloatField(default=0)

    def __unicode__(self):
        return 'Cuenta: %s | debe: %s | haber: %s' \
        % (self.cuenta.code, self.debe, self.haber)

    def actualizar_saldo_cuenta(self):
        b, created = Balanza.objects.get_or_create(cuenta=self.cuenta,
            periodo=self.periodo)
        b.saldo_final = b.get_saldo_final()
        b.save()

    def save(self, *args, **kwargs):
        self.periodo = self.comprobante.periodo
        super(Movimiento, self).save()
        self.actualizar_saldo_cuenta()
        c = Comprobante.objects.get(id=self.comprobante.id)
        c.calcular()

    #def delete(self, *args, **kwargs):
        #c = Comprobante.objects.get(id=self.comprobante.id)
        #b = Balanza.objects.get(cuenta=self.cuenta, periodo=self.periodo)
        #super(Movimiento, self).delete()
        #c.calcular()
        #b.actualizar_saldo()


class datos_documento(base):
    fecha = models.DateField(null=True, blank=True)
    numero = models.PositiveIntegerField(null=True, blank=True)
    periodo = models.ForeignKey(Periodo, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_periodo")
    user = models.ForeignKey(User, null=True, blank=True,
        related_name="%(app_label)s_%(class)s_user")

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
        n = 1
        model = self.__class__
        sets = model.objects.all()
        if sets:
            n += sets.aggregate(Max('numero'))['numero__max']
        return n

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = datetime.now()
        self.periodo = self.get_periodo(self.fecha)
        if not self.numero:
            self.numero = self.get_numero()
        super(datos_documento, self).save()


class Comprobante(datos_documento):
    concepto = models.TextField(max_length=400)
    code = models.CharField(max_length=30, null=True, blank=True)
    sucursal = models.CharField(max_length=65, null=True, blank=True)
    total_debe = models.FloatField(default=0)
    total_haber = models.FloatField(default=0)
    diferencia = models.FloatField(default=0)
    sumas_iguales = models.BooleanField(default=True)

    def movimientos(self):
        return Movimiento.objects.filter(comprobante=self)

    def detalle(self):
        return comprobante_detalle.objects.filter(
            comprobante=self).order_by('code')

    def actualizar_saldos_cuentas(self):
        if self.movimientos() and not self.periodo.cerrado:
            for m in self.movimientos():
                m.actualizar_saldo_cuenta()

    def get_total_debe(self):
        if self.movimientos():
            return self.movimientos().aggregate(Sum('debe'))['debe__sum']
        else:
            return 0

    def get_total_haber(self):
        if self.movimientos():
            return self.movimientos().aggregate(Sum('haber'))['haber__sum']
        else:
            return 0

    def comprobar(self):
        if self.total_debe == self.total_haber:
            self.sumas_iguales = True
        else:
            self.sumas_iguales = False
        self.diferencia = round(abs(self.total_debe - self.total_haber), 2)

    def calcular(self):
        if self.total_debe != self.get_total_debe():
            self.total_debe = self.get_total_debe()
            self.comprobar()
            self.save()
        if self.total_haber != self.get_total_haber():
            self.total_haber = self.get_total_haber()
            self.comprobar()
            self.save()

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = datetime.now()
        self.periodo = self.get_periodo(self.fecha)
        if not self.periodo.cerrado:
            if not self.numero:
                self.numero = self.get_numero()
            super(Comprobante, self).save()
            self.calcular()
            self.actualizar_saldos_cuentas()

    class Meta:
        verbose_name = 'comprobantes de diario'


class comprobante_detalle(models.Model):
    comprobante = models.ForeignKey(Comprobante)
    code = models.CharField(max_length=35, blank=True)
    name = models.CharField(max_length=100, blank=True)
    parcial = models.FloatField(blank=True, null=True)
    debe = models.FloatField(blank=True, null=True)
    haber = models.FloatField(blank=True, null=True)

    def top(self):
        top = 0
        for r in comprobante_detalle.objects.filter(
            comprobante=self.comprobante).order_by('code'):
                if r.id == self.id:
                    return 239 + (top * 20)
                top += 1

    def is_mayor(self):
        if len(self.code) <= 4:
            return True
        else:
            return False

    class Meta:
        managed = False
        db_table = 'contabilidad_comprobante_detalle'

    def save(self):
        pass

    def delete(self):
        pass


class migracion(models.Model):
    fecha = models.DateField()
    poliza = models.CharField(max_length=30, null=True, blank=True)
    concepto = models.TextField(max_length=400)
    sucursal = models.CharField(max_length=65, null=True, blank=True)
    numero_cuenta = models.CharField(max_length=30, null=True, blank=True)
    nombre_cuenta = models.CharField(max_length=65, null=True, blank=True)
    debe = models.FloatField(default=0)
    haber = models.FloatField(default=0)

    def get_comprobante(self):
        c, created = Comprobante.objects.get_or_create(code=self.poliza,
            concepto=self.concepto, fecha=self.fecha, sucursal=self.sucursal)
        return c

    def get_cuenta(self):
        c, created = Cuenta.objects.get_or_create(code=self.numero_cuenta,
            activo=True)
        c.name = self.nombre_cuenta
        c.save()
        return c

    def save(self, *args, **kwargs):
        m = Movimiento(comprobante=self.get_comprobante(),
            cuenta=self.get_cuenta(), debe=self.debe,
            haber=self.haber)
        m.save()

    class Meta:
        verbose_name = 'comprobante'
        verbose_name_plural = 'migracion de comprobantes'