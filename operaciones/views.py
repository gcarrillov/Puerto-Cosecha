from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import OperacionComercial
from .forms import OperacionForm
from productos.models import Producto


def es_empresa(user):
    return hasattr(user, 'perfil') and user.perfil.rol == 'empresa'


@login_required
def crear_operacion(request, producto_id):
    """
    Crear una operación comercial (importación/exportación) sobre un producto.
    Solo para usuarios con rol 'empresa'.
    """
    if not es_empresa(request.user):
        return HttpResponseForbidden("No tienes permiso para crear operaciones comerciales.")

    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        form = OperacionForm(request.POST)
        if form.is_valid():
            operacion = form.save(commit=False)
            operacion.empresa = request.user.perfil   # perfil de empresa
            operacion.producto = producto
            operacion.save()
            return redirect('mis_operaciones')
    else:
        form = OperacionForm()

    context = {
        'form': form,
        'producto': producto,
    }
    return render(request, 'operaciones/crear.html', context)


@login_required
def mis_operaciones(request):
    """
    Lista de operaciones comerciales de la empresa logueada.
    """
    if not es_empresa(request.user):
        return HttpResponseForbidden("No tienes permiso para ver estas operaciones.")

    operaciones = OperacionComercial.objects.filter(empresa=request.user.perfil).order_by('-fecha_creacion')
    return render(request, 'operaciones/mis_operaciones.html', {'operaciones': operaciones})
