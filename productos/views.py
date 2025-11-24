from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from operaciones.models import OperacionComercial
from .models import Producto, Incoterm, NormaComercial
from .forms import ProductoForm


def lista_productos(request):
    """
    Lista pública de productos.
    """
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})


def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    operaciones = OperacionComercial.objects.filter(producto=producto).prefetch_related('documentos')
    context = {
        'producto': producto,
        'operaciones': operaciones,
    }
    return render(request, 'productos/detalle.html', context)


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
def lista_incoterms(request):
    """
    Página de referencia general de Incoterms.
    """
    incoterms = Incoterm.objects.all().order_by("codigo")
    return render(request, "productos/incoterm_list.html", {"incoterms": incoterms})


def lista_normativa(request):
    """
    Página de referencia general de normativa comercial con filtros básicos.
    """
    pais = request.GET.get("pais", "")
    tipo = request.GET.get("tipo", "")

    normas = NormaComercial.objects.all()
    if pais:
        normas = normas.filter(pais__icontains=pais)
    if tipo:
        normas = normas.filter(tipo=tipo)

    context = {
        "normas": normas,
        "pais": pais,
        "tipo": tipo,
    }
    return render(request, "productos/norma_list.html", context)

