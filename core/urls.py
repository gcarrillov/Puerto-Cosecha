from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', RedirectView.as_view(url='/admin/', permanent=False)),   # redireccion para admin directo (solo para el desarrollo de la web)

    path(
        '',
        TemplateView.as_view(template_name='home.html'),
        name='home'
        ),

    # autenticacion / login
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='login'
        ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),   # se usa LOGOUT_REDIRECT_URL
        name='logout'
        ),
    # Productos
    path('productos/', include('productos.urls')),

    # Operaciones comerciales
    path('operaciones/', include('operaciones.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
