from django.views.generic.base import TemplateView
from moneycash.models import *


class TiendaPageView(TemplateView):
    template_name = "tienda/index.html"
    def get_context_data(self, **kwargs):
        ps = Producto.objects.all()
        context = super(TiendaPageView, self).get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['carrusel'] = []
        for p in ps[:5]:
            if p.imagen:
                context['carrusel'].append(p)
        context['featured'] = []
        for a in ps[5:15]:
            if a.imagen:
                context['featured'].append(a)
        context['bestseller'] = []
        for b in ps[15:]:
            if b.imagen:
                context['bestseller'].append(b)
        return context
