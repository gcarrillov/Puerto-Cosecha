from django.db import models
from usuarios.models import Usuario

class Producto(models.Model):
    UNIDADES = (
        ('kg', 'Kilogramo'),
        ('ton', 'Tonelada'),
        ('caja', 'Caja'),
        ('unidad', 'Unidad'),
    )

    CATEGORIAS = (
        ('fruta', 'Fruta'),
        ('hortaliza', 'Hortaliza'),
        ('grano', 'Grano'),
        ('otro', 'Otro'),
    )

    productor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    pais_origen = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name="Imagen del Producto")
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES, default='kg')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='fruta')
    certificaciones = models.TextField(blank=True, help_text="Certificaciones específicas del producto.")
    es_perecible = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.productor.user.username}"
