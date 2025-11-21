from django.db import models
from usuarios.models import Usuario
from productos.models import Producto

class OperacionComercial(models.Model):
    TIPO = (
        ('exportacion', 'Exportación'),
        ('importacion', 'Importación'),
    )

    ESTADO = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('en_transito', 'En tránsito'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    tipo_operacion = models.CharField(max_length=20, choices=TIPO)
    empresa = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='operaciones_empresa')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')
    incoterm = models.CharField(max_length=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_operacion} - {self.producto.nombre}"
