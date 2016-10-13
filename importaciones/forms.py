from django import forms
from .models import Importacion, Item


class ImportacionForm(forms.ModelForm):
    total_fob = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    utilidad = forms.FloatField(widget=forms.NumberInput(
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
        }))
    cip = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
    precio = forms.FloatField(widget=forms.NumberInput(
    attrs={
        'value': '0.0',
        'readonly': 'true',
        }))
