from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Usuario, Empresa, Productor

class RegistroProductorForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    email = forms.EmailField(label="Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    direccion = forms.CharField(max_length=255, required=False, label="Dirección")
    tipo_productor = forms.ChoiceField(choices=Productor.TIPO_PRODUCTOR, label="Tipo de productor")
    region = forms.CharField(max_length=100, required=False, label="Región")
    certificaciones = forms.CharField(widget=forms.Textarea, required=False, label="Certificaciones")
    capacidad_produccion_anual_ton = forms.DecimalField(
        required=False, max_digits=12, decimal_places=2, label="Capacidad producción anual (t)"
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya existe.")
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        if p1:
            validate_password(p1)
        return cleaned

class RegistroEmpresaForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    email = forms.EmailField(label="Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    direccion = forms.CharField(max_length=255, required=False, label="Dirección")
    razon_social = forms.CharField(max_length=150, label="Razón social")
    ruc = forms.CharField(max_length=20, label="RUC")
    pais = forms.CharField(max_length=50, label="País")
    tipo_empresa = forms.ChoiceField(choices=Empresa.TIPO_EMPRESA, label="Tipo de empresa")
    sitio_web = forms.URLField(required=False, label="Sitio web")
    contacto_comercial = forms.CharField(max_length=100, required=False, label="Contacto comercial")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya existe.")
        return username

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if Empresa.objects.filter(ruc=ruc).exists():
            raise ValidationError("Ya existe una empresa con ese RUC.")
        return ruc

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        if p1:
            validate_password(p1)
        return cleaned
