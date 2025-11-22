from django import forms
from .models import OperacionComercial


class OperacionForm(forms.ModelForm):
    class Meta:
        model = OperacionComercial
        # empresa y producto se asignan en la vista, no en el formulario
        fields = ['tipo_operacion', 'cantidad', 'incoterm', 'puerto_origen', 'puerto_destino', 'pais_destino', 'moneda']
