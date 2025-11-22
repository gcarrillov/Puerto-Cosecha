from django.db import models
from django.contrib.auth.models import User  
# IMPORTANTE:se esta usando el usuario de DJango como predeterminado , este modelo solo es un perfil asociado


class Usuario(models.Model):
    ROLES = (
        ('productor', 'Productor'),
        ('empresa', 'Empresa'),
        ('admin', 'Administrador'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"
class Empresa(models.Model):
    TIPO_EMPRESA = (
        ('importadora', 'Importadora'),
        ('exportadora', 'Exportadora'),
        ('mixta', 'Importadora/Exportadora'),
    )

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='empresa'
    )
    razon_social = models.CharField(max_length=150)
    ruc = models.CharField(max_length=20, unique=True)
    pais = models.CharField(max_length=50)
    tipo_empresa = models.CharField(max_length=20, choices=TIPO_EMPRESA, default='mixta')
    sitio_web = models.URLField(blank=True)
    contacto_comercial = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.razon_social} ({self.pais})"


class Productor(models.Model):
    TIPO_PRODUCTOR = (
        ('pequeno', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    )

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='productor'
    )
    tipo_productor = models.CharField(max_length=20, choices=TIPO_PRODUCTOR, default='pequeno')
    region = models.CharField(max_length=100, blank=True)
    certificaciones = models.TextField(blank=True, help_text="Certificaciones: orgánico, fair trade, etc.")
    capacidad_produccion_anual_ton = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Capacidad de producción anual en toneladas (opcional)."
    )

    def __str__(self):
        return f"Productor {self.usuario.user.username} - {self.tipo_productor}"
