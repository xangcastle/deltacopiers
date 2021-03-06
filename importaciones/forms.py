from django import forms
from .models import Importacion, Item


class ImportacionForm(forms.ModelForm):
    utilidad = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    total_cip = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    total_venta = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    total_dai = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    total_isc = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    total_iva = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    model = Importacion


class ItemForm(forms.ModelForm):
    model = Item
    cif = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }), label='costo cif')
    cip = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }), label='costo bodega destino')
    precio = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }), label='precio publico')
