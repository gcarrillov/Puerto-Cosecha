from django import forms
from .models import OperacionComercial


class OperacionForm(forms.ModelForm):
    class Meta:
        model = OperacionComercial
        # empresa y producto los asignado en la vista, no en el formulario
        fields = ['tipo_operacion', 'cantidad', 'incoterm']