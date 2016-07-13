from django.views.generic.base import TemplateView


class TiendaPageView(TemplateView):
    template_name = "tienda/index.html"
