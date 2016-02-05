from moneycash.models import Cuenta as base_cuenta


class Cuenta(base_cuenta):
    class Meta:
        proxy = True
