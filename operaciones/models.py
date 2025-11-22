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

    MONEDAS = (
        ('USD', 'Dólar estadounidense'),
        ('EUR', 'Euro'),
        ('PEN', 'Sol peruano'),
    )

    tipo_operacion = models.CharField(max_length=20, choices=TIPO)
    empresa = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='operaciones_empresa')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')
    incoterm = models.CharField(max_length=10)

    # Campos nuevos:
    puerto_origen = models.CharField(max_length=100, blank=True)
    puerto_destino = models.CharField(max_length=100, blank=True)
    pais_destino = models.CharField(max_length=50, blank=True)
    moneda = models.CharField(max_length=3, choices=MONEDAS, default='USD')
    precio_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monto total acordado para la operación."
    )
    fecha_salida = models.DateField(null=True, blank=True)
    fecha_llegada_estimada = models.DateField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_operacion} - {self.producto.nombre} - {self.empresa.user.username}"

class DocumentoAduanero(models.Model):
    TIPOS = (
        ('factura', 'Factura comercial'),
        ('packing_list', 'Packing List'),
        ('cert_fito', 'Certificado fitosanitario'),
        ('otros', 'Otros'),
    )

    operacion = models.ForeignKey(
        OperacionComercial,
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    archivo = models.FileField(upload_to='documentos_aduaneros/')
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - Operación {self.operacion.id}"
