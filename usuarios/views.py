from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

from .forms import RegistroProductorForm, RegistroEmpresaForm
from .models import Usuario, Productor, Empresa
from django.contrib.auth.decorators import login_required
from .decorators import rol_required


def registro_productor(request):
    if request.method == 'POST':
        form = RegistroProductorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password1']
            )
            perfil = Usuario.objects.create(
                user=user,
                rol='productor',
                telefono=data.get('telefono', ''),
                direccion=data.get('direccion', '')
            )
            Productor.objects.create(
                usuario=perfil,
                tipo_productor=data.get('tipo_productor'),
                region=data.get('region', ''),
                certificaciones=data.get('certificaciones', ''),
                capacidad_produccion_anual_ton=data.get('capacidad_produccion_anual_ton') or None
            )
            messages.success(request, "Registro de productor exitoso. Ya puedes iniciar sesión.")
            return redirect('usuarios:login')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = RegistroProductorForm()
    return render(request, 'auth/registro_productor.html', {'form': form})

def registro_empresa(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password1']
            )
            perfil = Usuario.objects.create(
                user=user,
                rol='empresa',
                telefono=data.get('telefono', ''),
                direccion=data.get('direccion', '')
            )
            Empresa.objects.create(
                usuario=perfil,
                razon_social=data.get('razon_social'),
                ruc=data.get('ruc'),
                pais=data.get('pais'),
                tipo_empresa=data.get('tipo_empresa'),
                sitio_web=data.get('sitio_web', ''),
                contacto_comercial=data.get('contacto_comercial', '')
            )
            messages.success(request, "Registro de empresa exitoso. Ya puedes iniciar sesión.")
            return redirect('usuarios:login')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = RegistroEmpresaForm()
    return render(request, 'auth/registro_empresa.html', {'form': form})

@login_required
@rol_required("productor")
def productor_dashboard(request):
    return render(request, 'auth/productor_dashboard.html')


@login_required
@rol_required("empresa")
def empresa_dashboard(request):
    return render(request, 'auth/empresa_dashboard.html')

@login_required
def redirigir_por_rol(request):
    perfil = request.user.perfil

    if perfil.rol == 'productor':
        return redirect('usuarios:productor_dashboard')

    if perfil.rol == 'empresa':
        return redirect('usuarios:empresa_dashboard')

    return redirect('/admin/')