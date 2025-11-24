from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('registro/productor/', views.registro_productor, name='registro_productor'),
    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),

    # opcional: páginas de dashboard por rol
    path('dashboard/productor/', views.productor_dashboard, name='productor_dashboard'),
    path('dashboard/empresa/', views.empresa_dashboard, name='empresa_dashboard'),

    path('redirigir/', views.redirigir_por_rol, name='redirigir_por_rol'),

]
