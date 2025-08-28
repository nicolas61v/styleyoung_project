"""
URL configuration for styleyoung_project project - StyleYoung Tienda Virtual

Configuración de URLs con separación completa:
- Usuario final: rutas desde /
- Administrador: rutas desde /admin-panel/
- Autenticación: rutas desde /auth/
- Django admin: /admin/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin (built-in)
    path('admin/', admin.site.urls),
    
    # Autenticación (usuarios y admins)
    path('auth/', include('usuarios.urls')),
    
    # Todas las rutas de la tienda (usuario final + admin-panel)
    path('', include('tienda.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
