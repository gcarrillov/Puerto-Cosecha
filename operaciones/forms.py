from django import forms
from .models import OperacionComercial


class OperacionForm(forms.ModelForm):

    class Meta:
        model = OperacionComercial

        # empresa y producto se asignan en la vista, no en el formulario
        fields = [
            'tipo_operacion',
            'cantidad',
            'incoterm',
            'puerto_origen',
            'puerto_destino',
            'pais_destino',
            'moneda',
        ]

        widgets = {
            'tipo_operacion': forms.Select(attrs={
                'class': 'form-select',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Cantidad de producto'
            }),
            'incoterm': forms.Select(attrs={
                'class': 'form-select'
            }),
            'puerto_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Callao'
            }),
            'puerto_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Rotterdam'
            }),
            'pais_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Países Bajos'
            }),
            'moneda': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    # ---------------------------
    # VALIDACIONES PERSONALIZADAS
    # ---------------------------
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return cantidad

    # Validación general
    def clean(self):
        cleaned_data = super().clean()
        
        origen = cleaned_data.get('puerto_origen')
        destino = cleaned_data.get('puerto_destino')

        if origen and destino and origen.lower() == destino.lower():
            raise forms.ValidationError("El puerto de origen y destino no pueden ser iguales.")

        return cleaned_data
