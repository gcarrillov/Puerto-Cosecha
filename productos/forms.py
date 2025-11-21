from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # productor lo setearemos en la vista, no desde el form (parte del frontend)
        fields = ['nombre', 'descripcion', 'precio_unitario', 'stock', 'pais_origen']
