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
        }), label='costo cip')
    precio = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }), label='precio publico')
