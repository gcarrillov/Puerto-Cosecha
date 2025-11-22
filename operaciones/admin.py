from django.contrib import admin
from .models import OperacionComercial, DocumentoAduanero

@admin.register(OperacionComercial)
class OperacionComercialAdmin(admin.ModelAdmin):
    list_display = ('tipo_operacion', 'empresa', 'producto', 'cantidad', 'estado', 'incoterm', 'fecha_creacion')
    list_filter = ('tipo_operacion', 'estado', 'incoterm', 'moneda')
    search_fields = ('empresa__user__username', 'producto__nombre')


@admin.register(DocumentoAduanero)
class DocumentoAduaneroAdmin(admin.ModelAdmin):
    list_display = ('operacion', 'tipo', 'fecha_subida')
    list_filter = ('tipo',)
    search_fields = ('operacion__empresa__user__username', 'operacion__producto__nombre')
