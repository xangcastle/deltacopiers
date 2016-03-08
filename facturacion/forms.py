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


class FacturaForm(forms.ModelForm):

    numero = forms.CharField(label='numero de factura', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    fecha = forms.CharField(label='fecha', max_length=50,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    code = forms.CharField(label='codigo del cliente', max_length=30,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    name = forms.CharField(label='nombre del cliente', max_length=125,
        widget=forms.TextInput(attrs={'class': 'datos_cliente',
            'autocomplete': 'off'}))

    identificacion = forms.CharField(label='identificacion del cliente',
        max_length=14, widget=forms.TextInput(attrs={'class': 'datos_cliente',
            'autocomplete': 'off'}))

    subtotal = forms.CharField(label='subtotal', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    descuento = forms.CharField(label='descuento', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    iva = forms.CharField(label='iva', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    ir = forms.CharField(label='retencion del ir', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    al = forms.CharField(label='retencion de la alcaldia', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    total = forms.CharField(label='total', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true'}))

    class Meta:
        model = Factura
        fields = ('numero', 'fecha', 'code', 'name', 'identificacion',
            'telefono', 'email', 'direccion', 'subtotal', 'descuento',
            'iva', 'ir', 'al', 'total')