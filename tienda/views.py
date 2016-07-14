from django.views.generic.base import TemplateView
from moneycash.models import *


class TiendaPageView(TemplateView):
    template_name = "tienda/index.html"
    def get_context_data(self, **kwargs):
        ps = Producto.objects.all()
        context = super(TiendaPageView, self).get_context_data(**kwargs)
        context['carrusel'] = []
        for p in ps[:5]:
            if p.imagen:
                context['carrusel'].append(p)
        context['featured'] = []
        for p in ps[5:15]:
            if p.imagen:
                context['featured'].append(p)
        return context
