# -*- coding: utf-8 -*-
from .models import *
from django import template

register = template.Library()


class Categorias(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<Categorias>"

    def render(self, context):
            context[self.varname] = Categoria.objects.all()
            return ''


@register.tag
def get_categorias(parser, token):
    """
        uso
            {% get_categorias as [varname]%}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_categorias' requiere de dos argumentos y se dieron %s"
            % (args))
    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_categorias' requiere que el primer argumento se 'as'")

    return Categorias(varname=tokens[2])

