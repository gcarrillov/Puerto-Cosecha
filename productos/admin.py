from django.contrib import admin
from .models import Producto, Incoterm, NormaComercial


@admin.register(Incoterm)
class IncotermAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre")
    search_fields = ("codigo", "nombre")


@admin.register(NormaComercial)
class NormaComercialAdmin(admin.ModelAdmin):
    list_display = ("pais", "tipo", "categoria_producto")
    list_filter = ("pais", "tipo")
    search_fields = ("pais", "categoria_producto")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'productor', 'precio_unitario', 'stock', 'pais_origen', 'fecha_registro')
    list_filter = ('pais_origen',)
    search_fields = ('nombre', 'productor__user__username')
    filter_horizontal = ("incoterms", "normas_comerciales")
