from django import models



AFECTACIONES = (
(1, "POSITIVA"),
(-1, "NEGATIVA"),
(0, "SIN AFECTACION"),
)


class TipoDoc(models.Model):
    name = models.CharField(max_length=65)
    afectacion = models.IntegerField(choices=AFECTACIONES)


class Documento(models.Model):
    numero = models.PositiveIntegerField()
    tipo = models.ForeingKey(TipoDoc)
    fecha = models.DateTimeField()
    cliente = models.ForeingKey('Cliente')


class Cliente(models.Model):
    identificacion = models.CharField(max_length=14, help_text="numero ruc")
