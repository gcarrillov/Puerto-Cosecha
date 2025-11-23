from django.urls import path
from .views import (
    crear_operacion,
    mis_operaciones,
    detalle_operacion,
    subir_documento,
    cambiar_estado,
    reporte_por_estado,
    reporte_por_pais,
    reporte_productos
)

urlpatterns = [
    # ----------------------
    # OPERACIONES
    # ----------------------
    path('crear/<int:producto_id>/', crear_operacion, name='crear_operacion'),
    path('mias/', mis_operaciones, name='mis_operaciones'),
    path('detalle/<int:operacion_id>/', detalle_operacion, name='detalle_operacion'),
    path('documento/subir/<int:operacion_id>/', subir_documento, name='subir_documento'),
    path('estado/<int:operacion_id>/<str:nuevo_estado>/', cambiar_estado, name='cambiar_estado'),

    # ----------------------
    # REPORTES
    # ----------------------
    path('reportes/estado/', reporte_por_estado, name='reporte_por_estado'),
    path('reportes/pais/', reporte_por_pais, name='reporte_por_pais'),
    path('reportes/productos/', reporte_productos, name='reporte_productos'),
]
