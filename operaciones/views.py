from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import models
from django.db.models import Sum, Count

from .models import OperacionComercial, DocumentoAduanero
from .forms import OperacionForm, DocumentoAduaneroForm
from productos.models import Producto


# -----------------------------------------------------------
#  Helper de permisos
# -----------------------------------------------------------

def es_empresa(user):
    """
    Verifica si el usuario autenticado pertenece al rol 'empresa'.
    """
    return hasattr(user, 'perfil') and user.perfil.rol == 'empresa'


# -----------------------------------------------------------
#  Crear operación comercial
# -----------------------------------------------------------

@login_required
def crear_operacion(request, producto_id):
    if not es_empresa(request.user):
        return HttpResponseForbidden("No tienes permiso para crear operaciones comerciales.")

    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        form = OperacionForm(request.POST)
        if form.is_valid():
            operacion = form.save(commit=False)

            # Empresa que compra / importa / exporta
            operacion.empresa = request.user.perfil  

            # Producto seleccionado
            operacion.producto = producto

            # Productor dueño del producto
            operacion.productor = producto.productor

            # El precio total se calcula dentro del modelo, en save()
            operacion.save()
            return redirect('mis_operaciones')

    else:
        form = OperacionForm()

    return render(request, 'operaciones/crear.html', {
        'form': form,
        'producto': producto,
    })



# -----------------------------------------------------------
#  Listar mis operaciones
# -----------------------------------------------------------

@login_required
def mis_operaciones(request):
    """
    Lista las operaciones comerciales de la empresa logueada.
    """

    operaciones = (
        OperacionComercial.objects
        .filter(empresa=request.user.perfil)
        .order_by('-fecha_creacion')
    )

    return render(request, 'operaciones/mis_operaciones.html', {'operaciones': operaciones})


# -----------------------------------------------------------
#  Detalle de operación comercial
# -----------------------------------------------------------

@login_required
def detalle_operacion(request, operacion_id):
    """
    Ver detalle completo de una operación:
    - Información
    - Estado
    - Documentos asociados
    - Formulario para subir documentos
    """
    operacion = get_object_or_404(OperacionComercial, pk=operacion_id)

    if operacion.empresa != request.user.perfil:
        return HttpResponseForbidden("No puedes ver esta operación.")

    documentos = operacion.documentos.all()
    form_doc = DocumentoAduaneroForm()

    context = {
        'operacion': operacion,
        'documentos': documentos,
        'form_doc': form_doc,
    }

    return render(request, 'operaciones/detalle.html', context)


# -----------------------------------------------------------
#  Subir documento aduanero
# -----------------------------------------------------------

@login_required
def subir_documento(request, operacion_id):
    """
    Permite a la empresa subir un documento aduanero asociado a una operación.
    """
    operacion = get_object_or_404(OperacionComercial, pk=operacion_id)

    if operacion.empresa != request.user.perfil:
        return HttpResponseForbidden("No tienes permiso para subir documentos para esta operación.")

    if request.method == 'POST':
        form = DocumentoAduaneroForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.operacion = operacion
            documento.save()

    return redirect('detalle_operacion', operacion_id=operacion_id)


# -----------------------------------------------------------
#  Cambiar estado de la operación
# -----------------------------------------------------------

@login_required
def cambiar_estado(request, operacion_id, nuevo_estado):
    """
    Actualiza el estado de la operación comercial.
    Flujo permitido:
      pendiente → en_proceso → en_transito → finalizado/cancelado
    """
    operacion = get_object_or_404(OperacionComercial, pk=operacion_id)

    if operacion.empresa != request.user.perfil:
        return HttpResponseForbidden("No tienes permiso para modificar esta operación.")

    ESTADOS_VALIDOS = ['pendiente', 'en_proceso', 'en_transito', 'finalizado', 'cancelado']

    if nuevo_estado not in ESTADOS_VALIDOS:
        return HttpResponseForbidden("Estado inválido.")

    operacion.estado = nuevo_estado
    operacion.save()

    return redirect('detalle_operacion', operacion_id=operacion_id)


# -----------------------------------------------------------
#  Reporte: operaciones por estado
# -----------------------------------------------------------

@login_required
def reporte_por_estado(request):
    """
    Genera un reporte agrupado por estado de operación.
    Permite filtrar por estado si se recibe un GET con 'estado'.
    """
    estado_filtrado = request.GET.get('estado', None)

    operaciones = OperacionComercial.objects.all()
    if estado_filtrado:
        operaciones = operaciones.filter(estado=estado_filtrado)

    # Agrupamos y contamos
    resumen = (
        operaciones.values('estado')
        .annotate(total=models.Count('id'))
        .order_by('estado')
    )

    estados = [e[0] for e in OperacionComercial.ESTADOS]

    return render(request, 'reportes/por_estado.html', {
        'resumen': resumen,
        'estados': estados,
        'estado_seleccionado': estado_filtrado,
    })


# -----------------------------------------------------------
#  Reporte: operaciones por país de destino
# -----------------------------------------------------------

@login_required
def reporte_por_pais(request):
    """
    Reporte de operaciones agrupadas por país de destino.
    Permite filtrar por país si se recibe un GET con 'pais'.
    """
    pais_filtrado = request.GET.get('pais', None)

    operaciones = OperacionComercial.objects.all()
    if pais_filtrado:
        operaciones = operaciones.filter(pais_destino=pais_filtrado)

    resumen = (
        operaciones.values('pais_destino')
        .annotate(total=models.Count('id'))
        .order_by('pais_destino')
    )

    paises = OperacionComercial.objects.values_list('pais_destino', flat=True).distinct()

    return render(request, 'reportes/por_pais.html', {
        'resumen': resumen,
        'paises': paises,
        'pais_seleccionado': pais_filtrado,
    })


# -----------------------------------------------------------
#  Reporte: productos más operados
# -----------------------------------------------------------

@login_required
def reporte_productos(request):
    """
    Reporte de operaciones filtradas por producto.
    """
    productos = Producto.objects.all()  # Para el dropdown
    producto_seleccionado = request.GET.get('producto')  # ID del producto

    if producto_seleccionado:
        operaciones = (
            OperacionComercial.objects
            .filter(producto_id=producto_seleccionado)
            .values('producto__nombre')
            .annotate(total=Sum('cantidad'))
        )
    else:
        operaciones = (
            OperacionComercial.objects
            .values('producto__nombre')
            .annotate(total=Sum('cantidad'))
            .order_by('-total')
        )

    context = {
        'productos': productos,
        'operaciones': operaciones,
        'producto_seleccionado': int(producto_seleccionado) if producto_seleccionado else None
    }
    return render(request, 'reportes/productos.html', context)
