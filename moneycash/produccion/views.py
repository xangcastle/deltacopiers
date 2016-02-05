# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def ProduccionPageView(request):
    template_name = "produccion/produccion.html"
    data = {}
    context = RequestContext(request)
    return render_to_response(template_name, data, context_instance=context)