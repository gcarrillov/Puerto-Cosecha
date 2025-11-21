from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'productor', 'precio_unitario', 'stock', 'pais_origen', 'fecha_registro')
    list_filter = ('pais_origen',)
    search_fields = ('nombre', 'productor__user__username')
