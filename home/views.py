from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "home/index.html"


class EncuentraBanproView(TemplateView):
    template_name = "home/encuentrabanpro.html"