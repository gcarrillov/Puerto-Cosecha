from django.db import models
from productos.models import Producto
from usuarios.models import Usuario


class OperacionComercial(models.Model):

    TIPOS = (
        ('IMP', 'Importación'),
        ('EXP', 'Exportación'),
    )

    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('en_transito', 'En tránsito'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    # --- TIPO ---
    tipo_operacion = models.CharField(max_length=3, choices=TIPOS)

    # --- ACTORES ---
    empresa = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='operaciones_empresa'
    )

    productor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='operaciones_productor'
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    # --- CANTIDAD / PRECIOS ---
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    # --- LOGÍSTICA ---
    incoterm = models.CharField(max_length=10)
    pais_destino = models.CharField(max_length=120)
    puerto_origen = models.CharField(max_length=120, blank=True, null=True)
    puerto_destino = models.CharField(max_length=120, blank=True, null=True)

    # --- ECONOMÍA ---
    moneda = models.CharField(max_length=10, default="USD")

    # --- ESTADO ---
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # =============================
    # VALIDACIONES + CÁLCULO
    # =============================
    def clean(self):
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")

        if self.producto.stock < self.cantidad:
            raise ValueError("Cantidad solicitada excede el stock disponible.")

    def calcular_precio_total(self):
        # Asumimos que Producto tiene precio_unitario
        self.precio_unitario = self.producto.precio_unitario
        self.precio_total = self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        self.clean()
        self.calcular_precicio_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_operacion_display()} - {self.producto.nombre} ({self.estado})"


# ====================================
# DOCUMENTOS ADUANEROS
# ====================================

class DocumentoAduanero(models.Model):
    TIPOS = (
        ('factura', 'Factura'),
        ('guia_remision', 'Guía de Remisión'),
        ('certificado_origen', 'Certificado de Origen'),
        ('otro', 'Otro'),
    )

    operacion = models.ForeignKey(
        OperacionComercial,
        on_delete=models.CASCADE,
        related_name='documentos'
    )

    tipo = models.CharField(max_length=50, choices=TIPOS)
    archivo = models.FileField(upload_to='documentos_aduaneros/')
    descripcion = models.TextField(blank=True)

    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - Op {self.operacion.id}"
