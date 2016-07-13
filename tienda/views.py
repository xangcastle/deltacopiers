from django.views.generic.base import TemplateView
from moneycash.models import *


class TiendaPageView(TemplateView):
    template_name = "tienda/index.html"
    def get_context_data(self, **kwargs):
        context = super(TiendaPageView, self).get_context_data(**kwargs)
        context['carrusel'] = []
        for p in Producto.objects.all()[:5]:
            if p.imagen:
                context['carrusel'].append(p)
        return context
