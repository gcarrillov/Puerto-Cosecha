from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', RedirectView.as_view(url='/admin/', permanent=False)),  # redireccion para admin directo (solo para el desarrollo de la web)
    path('', include('productos.urls')),
]
