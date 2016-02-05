from moneycash.models import models, Recibo as base_recibo,\
CierreCaja as base_cierre_caja, Deposito as base_deposito, detalle_pago,\
Factura as base_factura
from moneycash.manager import documento_impreso, documento_no_impreso


class Factura(base_factura):
    objects = models.Manager()
    objects = documento_impreso()

    class Meta:
        proxy = True
        verbose_name = "factura"
        verbose_name_plural = "facturas impresas"


class no_impresas(base_factura):
    objects = models.Manager()
    objects = documento_no_impreso()

    class Meta:
        proxy = True
        verbose_name = "factura"
        verbose_name_plural = "facturas no impresas"


class Recibo(base_recibo):
    class Meta:
        proxy = True


class efectivo_manager(models.Manager):
    def get_queryset(self):
        return super(efectivo_manager, self).get_queryset().filter(
            pago__code=1)


class cheque_manager(models.Manager):
    def get_queryset(self):
        return super(cheque_manager, self).get_queryset().filter(pago__code=2)


class tarjeta_manager(models.Manager):
    def get_queryset(self):
        return super(tarjeta_manager, self).get_queryset().filter(pago__code=3)


class credito_manager(models.Manager):
    def get_queryset(self):
        return super(credito_manager, self).get_queryset().filter(pago__code=4)


class transferencia_manager(models.Manager):
    def get_queryset(self):
        return super(transferencia_manager, self).get_queryset().filter(
            pago__code=5)


class abonos_manager(models.Manager):
    def get_queryset(self):
        return super(abonos_manager, self).get_queryset().exclude(
            factura__isnull=True)


class pago_efectivo(detalle_pago):
    objects = models.Manager()
    objects = efectivo_manager()

    class Meta:
        proxy = True
        verbose_name = 'monto'
        verbose_name_plural = 'pagos en efectivo'


class pago_cheque(detalle_pago):
    objects = models.Manager()
    objects = efectivo_manager()

    class Meta:
        proxy = True
        verbose_name = 'cheque'
        verbose_name_plural = 'pagos con cheque'


class pago_tarjeta(detalle_pago):
    objects = models.Manager()
    objects = efectivo_manager()

    class Meta:
        proxy = True
        verbose_name = 'transaccion'
        verbose_name_plural = 'pagos con tarjeta de credito'


class pago_credito(detalle_pago):
    objects = models.Manager()
    objects = efectivo_manager()

    class Meta:
        proxy = True
        verbose_name = 'cuenta'
        verbose_name_plural = 'cargos a cuentas de credito'


class pago_transferencia(detalle_pago):
    objects = models.Manager()
    objects = transferencia_manager()

    class Meta:
        proxy = True
        verbose_name = 'transaccion'
        verbose_name_plural = 'pagos via transferencia bancaria'


class abonos_factura(detalle_pago):
    objects = models.Manager()
    objects = abonos_manager()

    class Meta:
        proxy = True
        verbose_name = 'factura'
        verbose_name_plural = 'detalle de facturas canceladas'


class CierreCaja(base_cierre_caja):

    class Meta:
        proxy = True
        verbose_name = "cierre de caja"
        verbose_name_plural = "cierres de caja"


class Deposito(base_deposito):

    class Meta:
        proxy = True
