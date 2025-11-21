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
