# -*- coding: utf-8 -*-
from django import forms
from .models import *
from datetime import datetime


def default_fecha():
    return datetime.now()


class DetalleForm(forms.ModelForm):
    code = forms.CharField(label='codigo', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_code'}))

    name = forms.CharField(label='nombre', max_length=165,
        widget=forms.TextInput(attrs={'class': 'producto_name',
            'readonly': 'true'}))

    cantidad = forms.CharField(label='cantidad', max_length=14, initial=1,
        widget=forms.TextInput(attrs={'class': 'producto_cantidad'}))

    precio = forms.CharField(label='precio', max_length=14, initial=0.0,
        widget=forms.TextInput(attrs={'class': 'producto_precio',
            'readonly': 'true'}))

    descuento = forms.CharField(label='descuento', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_descuento'}))

    iva = forms.CharField(label='iva', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_iva',
            'readonly': 'true'}))

    producto_total = forms.CharField(label='total', max_length=14,
        widget=forms.TextInput(attrs={'class': 'producto_total',
            'readonly': 'true'}))

    class Meta:
        model = Detalle
        fields = ('code', 'name', 'cantidad', 'precio', 'descuento', 'iva',
            'producto_total')


class FacturaForm(forms.ModelForm):

    numero = forms.CharField(label='Numero de factura', max_length=14,
    required=False, widget=forms.TextInput(attrs={'readonly': 'true'}))

    fecha = forms.CharField(label='Fecha', max_length=50,
    required=False, widget=forms.TextInput(attrs={'readonly': 'true'}))

    code = forms.CharField(label='Codigo del cliente', max_length=30,
        required=False, widget=forms.TextInput(attrs={'readonly': 'true'}))

    name = forms.CharField(label='Nombre del cliente', max_length=125,  
        widget=forms.TextInput(attrs={'class': 'datos_cliente',
            'autocomplete': 'off', 'autofocus':'true',
            'required':'true'}))

    identificacion = forms.CharField(label='Identificacion del cliente',
        max_length=14, widget=forms.TextInput(attrs={'class': 'datos_cliente',
            'autocomplete': 'off', 'required':'true'}))

    telefono = forms.CharField(label='Telefono del cliente',
        max_length=25, widget=forms.TextInput(attrs={'class': 'datos_cliente',
            'autocomplete': 'off'}))

    email = forms.CharField(label='Email del cliente',
        max_length=80, widget=forms.EmailInput(attrs={'class': 'datos_cliente',
            'autocomplete': 'off'}))

    direccion = forms.CharField(label='Direcion del cliente',
        max_length=255, widget=forms.Textarea(attrs={'class': 'datos_cliente',
            'autocomplete': 'off'}))

    subtotal = forms.CharField(label='subtotal', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true',
        'value':'0.00'}))

    descuento = forms.CharField(label='descuento', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true',
        'value':'0.00'}))

    iva = forms.CharField(label='iva', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true',
        'value':'0.00'}))

    ir = forms.CharField(label='retencion del ir', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true',
        'value':'0.00'}))

    al = forms.CharField(label='retencion de la alcaldia', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true',
        'value':'0.00'}))

    total = forms.CharField(label='total', max_length=14,
        widget=forms.TextInput(attrs={'readonly': 'true',
         'value':'0.00'}))

    class Meta:
        model = Factura
        fields = ('numero', 'fecha', 'code', 'name', 'identificacion',
            'telefono', 'email', 'direccion', 'subtotal', 'descuento',
            'iva', 'ir', 'al', 'total')
