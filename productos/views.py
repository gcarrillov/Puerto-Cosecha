from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Producto
from .forms import ProductoForm


def lista_productos(request):
    """
    Lista pública de productos.
    """
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})


def detalle_producto(request, pk):
    """
    Detalle de un producto individual.
    """
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})


def es_productor(user):
    """
    Helper para verificar si el usuario autenticado es productor.
    """
    return hasattr(user, 'perfil') and user.perfil.rol == 'productor'


@login_required
def crear_producto(request):
    """
    Vista para que un productor cree un nuevo producto.
    """
    if not es_productor(request.user):
        return HttpResponseForbidden("No tienes permiso para crear productos.")

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignamos el productor desde el perfil del usuario logueado
            producto.productor = request.user.perfil
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/form.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_producto(request, pk):
    """
    Vista para que un productor edite SOLO sus propios productos.
    """
    producto = get_object_or_404(Producto, pk=pk)

    # Solo el productor dueño puede editarlo
    if not es_productor(request.user) or producto.productor != request.user.perfil:
        return HttpResponseForbidden("No tienes permiso para editar este producto.")

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('detalle_producto', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/form.html', {'form': form, 'accion': 'Editar'})
