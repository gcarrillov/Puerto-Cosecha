from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', RedirectView.as_view(url='/admin/', permanent=False)),  # redireccion para admin directo (solo para el desarrollo de la web)
    
    # auth
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='lista_productos'), name='logout'),

    # app productos
    path('', include('productos.urls')),
]
