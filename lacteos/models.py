from django.db import models
from django.db.models import Sum


def a_cordobas(numero):
    import locale
    locale.setlocale(locale.LC_ALL, 'es_NI.UTF-8')
    return locale.currency(numero, grouping=True)


class cliente(models.Model):
    nombre = models.CharField(max_length=200, help_text="NOMBRE DEL CLIENTE")
    ident = models.CharField(max_length=14, verbose_name="Identificacion",
        help_text="RUC/CEDULA")
    direccion = models.TextField(max_length=400, null=True, blank=True)
    telefono = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = "comprador"
        verbose_name_plural = "compradores"


class productor(models.Model):
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=200, null=True, blank=True)
    linea = models.ForeignKey('linea')
    precio = models.FloatField(null=True, blank=True,
        verbose_name="Precio Pactado")
    exento = models.BooleanField(default=False)

    def precio_pago(self):
        if self.precio:
            return self.precio
        else:
            return self.linea.precio

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "productores"
        ordering = ['nombre']


class linea(models.Model):
    nombre = models.CharField(max_length=200)
    recolector = models.CharField(max_length=200)
    precio = models.FloatField(verbose_name="Precio de la Linea")

    def __unicode__(self):
        return self.nombre

    def productores(self):
        return productor.objects.filter(linea=self)

    def lista_productores(self):
        return '<a href="/lacteos/print/productores/%s/" class="btn btn-primary btn-xs glyphicon glyphicon-print" target="_blank">  Productores</a>' % (self.id)

    lista_productores.allow_tags = True

    class Meta:
        ordering = ['nombre']


class periodo_manager(models.Manager):
    def get_queryset(self):
        return super(periodo_manager,
            self).get_queryset().filter(cerrado=False)


class periodo(models.Model):
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    cerrado = models.BooleanField(default=False)
    objects = models.Manager()
    objects = periodo_manager()

    def __unicode__(self):
        return str(self.fecha_final)

    def recolecciones(self):
        return recoleccion.objects.filter(periodo=self)

    def total_recolectado(self):
        total = 0.0
        for d in self.recolecciones():
            total += d.total_recolectado()
        return total

    def total_ir(self):
        total = 0.0
        for d in self.recolecciones():
            total += d.total_ir()
        return total

    def total_bacsa(self):
        total = 0.0
        for d in self.recolecciones():
            total += d.total_bacsa()
        return total

    def total_retencion(self):
        total = 0.0
        for d in self.recolecciones():
            total += d.total_retencion()
        return total

    def total_prestamos(self):
        ade = adelanto.objects.filter(periodo=self,
            tipo='PR').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_veterinaria(self):
        ade = adelanto.objects.filter(periodo=self,
            tipo='VE').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_ferreteria(self):
        ade = adelanto.objects.filter(periodo=self,
            tipo='FE').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_abarrotes(self):
        ade = adelanto.objects.filter(periodo=self,
            tipo='AB').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_deducciones(self):
        total = 0.0
        for d in self.recolecciones():
            total += d.total_deducciones()
        return total

    def total_pagado(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_pagado()
        return total

    def resumen_recoleccion(self):
        return '<a href="/lacteos/print/resumen_recoleccion/%s/" class="btn btn-default btn-xs glyphicon glyphicon-print" target="_blank">  Resumen Recoleccion</a>' % (self.id)

    resumen_recoleccion.allow_tags = True

    def resumen_pago(self):
        return '<a href="/lacteos/print/resumen_pago/%s/" class="btn btn-default btn-xs glyphicon glyphicon-print" target="_blank">  Resumen Pagos</a>' % (self.id)

    resumen_pago.allow_tags = True

    def total_dia_1(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_1()
        return total

    def total_dia_2(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_2()
        return total

    def total_dia_3(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_3()
        return total

    def total_dia_4(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_4()
        return total

    def total_dia_5(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_5()
        return total

    def total_dia_6(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_6()
        return total

    def total_dia_7(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_dia_7()
        return total

    class Meta:
        ordering = ['fecha_inicial']


class recoleccion(models.Model):
    periodo = models.ForeignKey(periodo)
    linea = models.ForeignKey(linea)

    def cerrado(self):
        return self.periodo.cerrado

    def __unicode__(self):
        return str(self.periodo.fecha_final) + ' ' + str(self.linea.nombre)

    def productores_linea(self):
        return productor.objects.filter(linea=self.linea)

    def detalles(self):
        return detalle.objects.filter(recoleccion=self)

    def total_recolectado(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_recolectado()
        return total

    def total_ir(self):
        total = 0.0
        for d in self.detalles():
            total += d.ir()
        return total

    def total_bacsa(self):
        total = 0.0
        for d in self.detalles():
            total += d.bacsa()
        return total

    def total_retencion(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_retencion()
        return total

    def total_prestamos(self):
        ade = adelanto.objects.filter(periodo=self.periodo,productor__in=self.productores_linea(),tipo='PR').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_veterinaria(self):
        ade = adelanto.objects.filter(periodo=self.periodo,productor__in=self.productores_linea(),tipo='VE').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_ferreteria(self):
        ade = adelanto.objects.filter(periodo=self.periodo,productor__in=self.productores_linea(),tipo='FE').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_abarrotes(self):
        ade = adelanto.objects.filter(periodo=self.periodo,productor__in=self.productores_linea(),tipo='AB').aggregate(Sum('monto'))['monto__sum']
        if ade:
            return ade
        else:
            return 0

    def total_deducciones(self):
        total = 0.0
        for d in self.detalles():
            total += d.total_deducciones()
        return total

    def total_pagado(self):
        total = 0.0
        for d in self.detalles():
            total += d.neto_recibir()
        return total

    def imprimir(self):
        return '<a href="/lacteos/print/recibos/%s/" class="btn btn-primary btn-xs glyphicon glyphicon-print imprimir_recibos" target="_blank" data-id="%s">  Imprimir Recibos</a>' % (self.id, self.id)

    imprimir.allow_tags = True

    def retenciones(self):
        return '<a href="/lacteos/print/retenciones/%s/" class="btn btn-primary btn-xs glyphicon glyphicon-print" target="_blank">  Imprimir Retenciones</a>' % (self.id)

    retenciones.allow_tags = True

    def detalle_linea(self):
        return '<a href="/lacteos/print/detalle_linea/%s/" class="btn btn-default btn-xs glyphicon glyphicon-print" target="_blank">  Detalle Linea</a>' % (self.id)

    detalle_linea.allow_tags = True

    def total_dia_1(self):
        return self.detalles().aggregate(Sum('dia_1'))['dia_1__sum']

    def total_dia_2(self):
        return self.detalles().aggregate(Sum('dia_2'))['dia_2__sum']

    def total_dia_3(self):
        return self.detalles().aggregate(Sum('dia_3'))['dia_3__sum']

    def total_dia_4(self):
        return self.detalles().aggregate(Sum('dia_4'))['dia_4__sum']

    def total_dia_5(self):
        return self.detalles().aggregate(Sum('dia_5'))['dia_5__sum']

    def total_dia_6(self):
        return self.detalles().aggregate(Sum('dia_6'))['dia_6__sum']

    def total_dia_7(self):
        return self.detalles().aggregate(Sum('dia_7'))['dia_7__sum']

    class Meta:
        verbose_name_plural = "recolecciones"
        ordering = ['linea']

    def actualizar_precio(self):
        if not self.cerrado():
            for p in self.detalles():
                p.precio = p.productor.precio_pago()
                p.save()


class detalle(models.Model):
    recoleccion = models.ForeignKey(recoleccion)
    productor = models.ForeignKey(productor)
    dia_1 = models.IntegerField(default=0)
    dia_2 = models.IntegerField(default=0)
    dia_3 = models.IntegerField(default=0)
    dia_4 = models.IntegerField(default=0)
    dia_5 = models.IntegerField(default=0)
    dia_6 = models.IntegerField(default=0)
    dia_7 = models.IntegerField(default=0)
    dia_8 = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    precio = models.FloatField(null=True, default=0)

    def to_json(self):
        obj = {}
        obj['periodo'] = self.detalle_periodo()
        obj['productor'] = self.productor.nombre
        obj['dia_1'] = str(self.dia_1)
        obj['dia_2'] = str(self.dia_2)
        obj['dia_3'] = str(self.dia_3)
        obj['dia_4'] = str(self.dia_4)
        obj['dia_5'] = str(self.dia_5)
        obj['dia_6'] = str(self.dia_6)
        obj['dia_7'] = str(self.dia_7)
        obj['dia_8'] = str(self.dia_8)
        obj['produccion'] = str(self.total_recolectado())
        obj['precio'] =str(self.precio)
        obj['subtotal'] =str(self.subtotal())
        obj['retencion'] =str(self.total_retencion())
        obj['total'] =str(self.total_pago())
        obj['prestamos'] =str(self.total_prestamos())
        obj['ferreteria'] =str(self.total_ferreteria())
        obj['veterinaria'] =str(self.total_veterinaria())
        obj['abarrotes'] =str(self.total_abarrotes())
        obj['neto_recibir'] =str(self.neto_recibir())
        return obj

    def __unicode__(self):
        return self.productor.nombre

    def periodo(self):
        return self.recoleccion.periodo

    def fecha_inicial(self):
        return self.periodo().fecha_inicial

    def fecha_final(self):
        return self.periodo().fecha_final

    def detalle_periodo(self):
      return "SEMANA DEL: %s AL %s " % (self.fecha_inicial(), self.fecha_final())

    def total_recolectado(self):
        return self.dia_1 + self.dia_2 + self.dia_3 + self.dia_4 + self.dia_5 + self.dia_6 + self.dia_7

    def total_pago(self):
        return self.total_recolectado() * self.precio

    def ir(self):
        if self.productor.exento:
            return 0.0
        else:
            return self.total_pago() * 0.01

    def bacsa(self):
        if self.productor.exento:
            return 0.0
        else:
            return self.total_pago() * 0.0025

    def total_retencion(self):
        return round(self.ir() + self.bacsa(), 2)

    def subtotal(self):
        return round(self.total_pago() - self.total_retencion(), 2)

    def prestamos(self):
        return adelanto.objects.filter(periodo=self.periodo(),productor=self.productor,tipo='PR')

    def total_prestamos(self):
        if self.productor.linea == self.recoleccion.linea and self.prestamos():
            return self.prestamos().aggregate(Sum('monto'))['monto__sum']
        else:
            return 0

    def veterinaria(self):
        return adelanto.objects.filter(periodo=self.periodo(),productor=self.productor,tipo='VE')

    def total_veterinaria(self):
        if self.productor.linea == self.recoleccion.linea and self.veterinaria():
            return self.veterinaria().aggregate(Sum('monto'))['monto__sum']
        else:
            return 0

    def ferreteria(self):
        return adelanto.objects.filter(periodo=self.periodo(),productor=self.productor,tipo='FE')

    def total_ferreteria(self):
        if self.productor.linea == self.recoleccion.linea and self.ferreteria():
            return self.ferreteria().aggregate(Sum('monto'))['monto__sum']
        else:
            return 0

    def abarrotes(self):
        return adelanto.objects.filter(periodo=self.periodo(),productor=self.productor,tipo='AB')

    def total_abarrotes(self):
        if self.productor.linea == self.recoleccion.linea and self.abarrotes():
            return self.abarrotes().aggregate(Sum('monto'))['monto__sum']
        else:
            return 0

    def total_deducciones(self):
        if self.productor.linea == self.recoleccion.linea and adelanto.objects.filter(periodo=self.periodo(),productor=self.productor):
            return adelanto.objects.filter(periodo=self.periodo(),productor=self.productor).aggregate(Sum('monto'))['monto__sum']
        else:
            return 0

    def neto_recibir(self):
        return a_cordobas(round(self.subtotal() - self.total_deducciones(),2))

    def save(self, *args, **kwars):
        self.total = self.total_recolectado()
        super(detalle, self).save()

    class Meta:
        verbose_name = "productor"
        verbose_name_plural = "detalle de recoleccion"
        ordering = ['productor']


class adelanto(models.Model):
    TIPO_CHOICES = (
                    ('PR', 'PRESTAMOS'),
                    ('VE', 'VETERINARIA'),
                    ('FE', 'FERRETERIA'),
                    ('AB', 'ABARROTES'),
                    )
    periodo = models.ForeignKey(periodo)
    productor = models.ForeignKey(productor)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    monto = models.FloatField()
    comentario = models.TextField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.productor. nombre + ' ' + str(self.monto)

    class Meta:
        ordering = ['productor',]


class entrega(models.Model):
    fecha = models.DateTimeField()
    periodo = models.ForeignKey(periodo,null=True)
    cliente = models.ForeignKey(cliente)
    precio = models.FloatField()
    cantidad = models.FloatField()

    def save(self):
        try:
            p = periodo.objects.filter(cerrado=False)[0]
            if p:
                self.periodo = p
        except:
            pass
        super(entrega,self).save()
