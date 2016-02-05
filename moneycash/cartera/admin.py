from moneycash.admin import admin, entidad_admin
from moneycash.cartera.models import Cuenta

admin.site.register(Cuenta, entidad_admin)
