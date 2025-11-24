from django.db import models
from usuarios.models import Usuario


class Incoterm(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # FOB, CIF, EXW, etc.
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    obligaciones_vendedor = models.TextField(blank=True)
    obligaciones_comprador = models.TextField(blank=True)

    class Meta:
        verbose_name = "Incoterm"
        verbose_name_plural = "Incoterms"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class NormaComercial(models.Model):
    TIPO_CHOICES = [
        ("EXP", "Exportación"),
        ("IMP", "Importación"),
        ("AMB", "Ambos"),
    ]

    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    pais = models.CharField(max_length=100)
    categoria_producto = models.CharField(
        max_length=100,
        blank=True,
        help_text="Opcional. Ej: Frutas, Granos, Café, etc."
    )
    descripcion = models.TextField()
    enlace_oficial = models.URLField(blank=True)

    class Meta:
        verbose_name = "Norma comercial"
        verbose_name_plural = "Normas comerciales"
        ordering = ["pais", "tipo"]

    def __str__(self):
        base = f"{self.pais} - {self.get_tipo_display()}"
        if self.categoria_producto:
            base += f" ({self.categoria_producto})"
        return base

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

    incoterms = models.ManyToManyField(
        Incoterm,
        blank=True,
        related_name="productos",
        help_text="Incoterms aplicables a este producto"
    )
    normas_comerciales = models.ManyToManyField(
        NormaComercial,
        blank=True,
        related_name="productos",
        help_text="Normativa comercial asociada al producto"
    )


    def __str__(self):
        return f"{self.nombre} - {self.productor.user.username}"
