from django.urls import path
from .views import crear_operacion, mis_operaciones

urlpatterns = [
    path('crear/<int:producto_id>/', crear_operacion, name='crear_operacion'),
    path('mias/', mis_operaciones, name='mis_operaciones'),
]
