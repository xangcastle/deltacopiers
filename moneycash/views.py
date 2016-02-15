from django.views.generic.base import TemplateView


class HomePage(TemplateView):
    template_name = "moneycash/index.html"

class ModulesPage(TemplateView):
    template_name = "moneycash/modules.html"
