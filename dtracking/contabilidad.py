
from django import models



class Periodo(models.Model):
    fecha_inicio =
    fecha_inicio =
    cerrado = models.BooleanField()

class Base(models.Model):
    codigo
    name


class Cuenta(Base):
    parent = models.ForeingKey('self')


class Comprobante(models.Model):
    periodo = models.ForeingKey(Periodo)
    fecha
    numero
    TipoDoc


class Movimiento(models.Model):
    cuenta = models.ForeingKey(Cuenta)
    debe = models.FloatField()
    debe = models.FloatField()


class Banco(Base):
    pass


class cuenta_periodo(models.Model):
    cuenta = models.ForeingKey(Cuenta)
    periodo = models.ForeingKey(Periodo)
    saldo_inicial = models.FloatField()
    saldo_final = models.FloatField()
