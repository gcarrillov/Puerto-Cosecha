from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import Producto
from .forms import ProductoForm
from operaciones.models import OperacionComercial  # para mostrar operaciones del producto


# -----------------------------------------------------------
#  Helpers de permisos
# -----------------------------------------------------------

def es_productor(user):
    """
    Verifica si el usuario autenticado pertenece al rol 'productor'.
    Maneja también el caso donde el usuario no tiene perfil.
    """
    try:
        return hasattr(user, 'perfil') and user.perfil.rol == 'productor'
    except ObjectDoesNotExist:
        return False


def es_empresa(user):
    """
    Verifica si el usuario autenticado pertenece al rol 'empresa'.
    Maneja también el caso donde el usuario no tiene perfil.
    """
    try:
        return hasattr(user, 'perfil') and user.perfil.rol == 'empresa'
    except ObjectDoesNotExist:
        return False


# -----------------------------------------------------------
#  Listado de productos (catálogo)
# -----------------------------------------------------------

def lista_productos(request):
    """
    Muestra el catálogo de productos disponibles.
    """
    productos = (
        Producto.objects
        .select_related('productor')
        .all()
    )

    return render(request, 'productos/lista.html', {
        'productos': productos,
    })


# -----------------------------------------------------------
#  Detalle de producto + lógica para "Adquirir"
# -----------------------------------------------------------

def detalle_producto(request, pk):
    """
    Muestra la ficha completa de un producto y calcula si el usuario
    puede o no adquirirlo, y si es dueño del producto.
    """
    producto = get_object_or_404(Producto, pk=pk)

    puede_adquirir = False
    motivo_bloqueo = None
    es_duenio = False

    # Operaciones asociadas a este producto
    operaciones = (
        OperacionComercial.objects
        .filter(producto=producto)
        .select_related('empresa', 'empresa__user')
        .prefetch_related('documentos')
    )

    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
        except ObjectDoesNotExist:
            motivo_bloqueo = "Debes completar tu perfil para adquirir productos."
        else:
            # ¿Es dueño del producto?
            es_duenio = (perfil == producto.productor)

            if es_duenio:
                motivo_bloqueo = "No puedes adquirir un producto que tú mismo ofreces."
            elif perfil.rol != 'empresa':
                motivo_bloqueo = "Solo los usuarios con rol 'empresa' pueden adquirir productos."
            else:
                # Empresa válida y distinta al productor
                puede_adquirir = True

    context = {
        'producto': producto,
        'operaciones': operaciones,
        'puede_adquirir': puede_adquirir,
        'motivo_bloqueo': motivo_bloqueo,
        'es_duenio': es_duenio,
    }
    return render(request, 'productos/detalle.html', context)


# -----------------------------------------------------------
#  Crear producto (solo productores)
# -----------------------------------------------------------

@login_required
def crear_producto(request):
    """
    Permite a un productor registrar un nuevo producto.
    """
    if not es_productor(request.user):
        return HttpResponseForbidden(
            "Solo los usuarios con rol 'productor' pueden crear productos."
        )

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignamos el productor desde el perfil del usuario
            producto.productor = request.user.perfil
            producto.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/crear.html', {
        'form': form,
    })


# -----------------------------------------------------------
#  Editar producto (solo el productor dueño)
# -----------------------------------------------------------

@login_required
def editar_producto(request, pk):
    """
    Permite a un productor editar uno de sus productos.
    """
    producto = get_object_or_404(Producto, pk=pk)

    try:
        perfil = request.user.perfil
    except ObjectDoesNotExist:
        return HttpResponseForbidden("No tienes un perfil asociado para editar productos.")

    if perfil != producto.productor:
        return HttpResponseForbidden("No puedes editar un producto que no te pertenece.")

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('detalle_producto', pk=producto.id)
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar.html', {
        'form': form,
        'producto': producto,
    })


# -----------------------------------------------------------
#  Eliminar producto (solo el productor dueño)
# -----------------------------------------------------------

@login_required
def eliminar_producto(request, pk):
    """
    Permite a un productor eliminar uno de sus productos.
    """
    producto = get_object_or_404(Producto, pk=pk)

    try:
        perfil = request.user.perfil
    except ObjectDoesNotExist:
        return HttpResponseForbidden("No tienes un perfil asociado para eliminar productos.")

    if perfil != producto.productor:
        return HttpResponseForbidden("No puedes eliminar un producto que no te pertenece.")

    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('lista_productos')

    # Confirmación simple
    return render(request, 'productos/eliminar_confirmacion.html', {
        'producto': producto,
    })


# -----------------------------------------------------------
#  Lista de Incoterms (Módulo Anthony)
# -----------------------------------------------------------

def lista_incoterms(request):
    """
    Vista placeholder para listar incoterms.
    Aquí luego pueden cargar el modelo real de Incoterms.
    """
    # Por ahora no hacemos query a un modelo específico para no romper
    return render(request, 'productos/lista_incoterms.html', {})


# -----------------------------------------------------------
#  Lista de Normativa comercial (Módulo Anthony)
# -----------------------------------------------------------

def lista_normativa(request):
    """
    Vista placeholder para listar normativa comercial.
    Aquí luego pueden cargar el modelo real de normativa.
    """
    return render(request, 'productos/lista_normativa.html', {})
