"""
URL configuration for styleyoung_project project - StyleYoung Tienda Virtual

MAPA DE RUTAS COMPLETO:
======================

🛍️ USUARIO FINAL (/)
- / → Home page  
- /productos/ → Catálogo productos
- /producto/<id>/ → Detalle producto
- /carrito/ → Carrito de compras
- /mis-pedidos/ → Historial pedidos

👨‍💼 ADMINISTRADOR (/admin-panel/)
- /admin-panel/ → Dashboard admin
- /admin-panel/productos/ → Gestión productos  
- /admin-panel/categorias/ → Gestión categorías
- /admin-panel/pedidos/ → Gestión pedidos
- /admin-panel/reportes/ → Reportes y análisis

🔐 AUTENTICACIÓN (/auth/)
- /auth/login/ → Login usuario
- /auth/registro/ → Registro usuario
- /auth/logout/ → Cerrar sesión
- /auth/admin-auth/login/ → Login admin

🔧 DJANGO ADMIN
- /admin/ → Panel Django admin

📡 APIs AJAX
- /api/busqueda/ → Búsqueda en tiempo real
- /api/actualizar-ventas/ → Actualizar contadores
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import JsonResponse

def api_status(request):
    """Endpoint para verificar estado de la API"""
    return JsonResponse({
        'status': 'online',
        'project': 'StyleYoung',
        'version': '1.0.0',
        'routes': {
            'user': '/',
            'admin': '/admin-panel/', 
            'auth': '/auth/',
            'api': '/api/'
        }
    })

urlpatterns = [
    # Django Admin (built-in)
    path('admin/', admin.site.urls),

    # API Status endpoint
    path('api/status/', api_status, name='api_status'),

    # Language switcher
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs with internationalization support
urlpatterns += i18n_patterns(
    # Autenticación (usuarios y admins)
    path('auth/', include('usuarios.urls')),

    # Todas las rutas de la tienda (usuario final + admin-panel)
    path('', include('tienda.urls')),
)

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
