# -*- coding: utf-8 -*-
from django import forms
from .models import *


class DetalleForm(forms.ModelForm):
    code = forms.CharField(label='codigo', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_code'}))

    name = forms.CharField(label='nombre', max_length=165,
        widget=forms.TextInput(attrs={'class': 'producto_name',
            'readonly': 'true'}))

    cantidad = forms.CharField(label='cantidad', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_cantidad'}))

    precio = forms.CharField(label='precio', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_precio',
            'readonly': 'true'}))

    descuento = forms.CharField(label='descuento', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_descuento'}))

    iva = forms.CharField(label='iva', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_iva',
            'readonly': 'true'}))

    total = forms.CharField(label='total', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_total',
            'readonly': 'true'}))

    class Meta:
        model = Detalle
        fields = ('code', 'name', 'cantidad', 'precio', 'descuento', 'iva',
            'total')