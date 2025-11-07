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

📡 API REST (v1)
- /api/v1/ → Documentación de la API
- /api/v1/productos/ → Lista de productos
- /api/v1/productos/{id}/ → Detalle de producto
- /api/v1/productos/en-stock/ → Productos con stock
- /api/v1/productos/mas-vendidos/ → Top productos
- /api/v1/categorias/ → Lista de categorías
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import JsonResponse
from django.views.i18n import set_language

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

def home_redirect(request):
    """Redirecciona a la página de inicio con el idioma configurado"""
    from django.shortcuts import redirect
    from django.utils.translation import get_language
    lang = get_language() or 'es'  # Default a español
    return redirect(f'/{lang}/')

urlpatterns = [
    # Redirección de raíz a idioma por defecto
    path('', home_redirect, name='home_redirect'),

    # Django Admin (built-in)
    path('admin/', admin.site.urls),

    # API REST v1 (pública para consumo externo)
    path('api/v1/', include('tienda.api_urls')),

    # API Status endpoint
    path('api/status/', api_status, name='api_status'),

    # Language switcher
    path('i18n/', include('django.conf.urls.i18n')),
]

# API REST (sin internacionalización)
from rest_framework.routers import DefaultRouter
from tienda.views import ProductoViewSet

api_router = DefaultRouter()
api_router.register(r'productos', ProductoViewSet, basename='producto-api')

urlpatterns += [
    path('api/v1/', include(api_router.urls)),
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
