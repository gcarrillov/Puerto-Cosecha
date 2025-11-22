from django.contrib import admin
from .models import Usuario, Empresa, Productor

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefono', 'direccion')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email', 'telefono')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'ruc', 'pais', 'tipo_empresa')
    search_fields = ('razon_social', 'ruc', 'usuario__user__username')


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_productor', 'region')
    search_fields = ('usuario__user__username', 'region')
