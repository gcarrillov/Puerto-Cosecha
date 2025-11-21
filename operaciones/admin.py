from django.contrib import admin
from .models import OperacionComercial


@admin.register(OperacionComercial)
class OperacionComercialAdmin(admin.ModelAdmin):
    list_display = ('tipo_operacion', 'empresa', 'producto', 'cantidad', 'estado', 'incoterm', 'fecha_creacion')
    list_filter = ('tipo_operacion', 'estado', 'incoterm')
    search_fields = ('empresa__user__username', 'producto__nombre')
