from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # HOME (inicio)
    path(
        '',
        TemplateView.as_view(template_name='home.html'),
        name='home'
    ),
    path('admin/', admin.site.urls),

    # AUTENTICACIÓN (login/logout)
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # REGISTROS (productor/empresa)
    path('accounts/', include('usuarios.urls')),

    # Productos
    path('productos/', include('productos.urls')),

    # Operaciones
    path('operaciones/', include('operaciones.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
