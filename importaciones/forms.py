from django import forms
from .models import Importacion


class ImportacionForm(forms.ModelForm):
    total_fob = forms.FloatField(widget=forms.NumberInput(attrs={'value': '0.0'}))
    model = Importacion
