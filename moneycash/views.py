from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from moneycash.models import MyUser


class HomePage(TemplateView):
    template_name = "moneycash/base.html"


class FacturacionPage(TemplateView):
    template_name = "moneycash/facturacion.html"


def register_empresa(request):
    user = MyUser.objects.get(id=request.user.id)
    empresa = user.get_empresa(request.POST.get('razon_social', ''))
    empresa.numero_ruc = request.POST.get('numero_ruc', '')
    empresa.direccion = request.POST.get('direccion', '')
    empresa.email = request.POST.get('email', '')
    empresa.save()
    user.empresa = empresa
    user.save()
    return HttpResponseRedirect("/moneycash")