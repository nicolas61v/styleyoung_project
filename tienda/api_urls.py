"""
URLs para la API REST de StyleYoung

API base: /api/v1/
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .api_views import ProductoViewSet, CategoriaViewSet

# Router de DRF para generar automáticamente las URLs
router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'categorias', CategoriaViewSet, basename='categoria')


@api_view(['GET'])
def api_root(request):
    """
    Endpoint raíz de la API que muestra todos los endpoints disponibles

    GET /api/v1/
    """
    return Response({
        'mensaje': 'Bienvenido a la API de StyleYoung - Tienda Virtual de Ropa',
        'version': '1.0',
        'proyecto': 'StyleYoung',
        'documentacion': request.build_absolute_uri('/api/v1/docs/'),
        'endpoints': {
            'productos': {
                'lista': request.build_absolute_uri(reverse('api:producto-list')),
                'en_stock': request.build_absolute_uri('/api/v1/productos/en-stock/'),
                'mas_vendidos': request.build_absolute_uri('/api/v1/productos/mas-vendidos/'),
                'estadisticas': request.build_absolute_uri('/api/v1/productos/estadisticas/'),
                'detalle': request.build_absolute_uri('/api/v1/productos/{id}/'),
            },
            'categorias': {
                'lista': request.build_absolute_uri(reverse('api:categoria-list')),
                'detalle': request.build_absolute_uri('/api/v1/categorias/{id}/'),
                'productos_categoria': request.build_absolute_uri('/api/v1/categorias/{id}/productos/'),
            },
        },
        'parametros_busqueda': {
            'search': 'Buscar en nombre, marca, descripción, color, material',
            'categoria': 'Filtrar por ID de categoría',
            'marca': 'Filtrar por marca exacta',
            'color': 'Filtrar por color exacto',
            'precio_min': 'Precio mínimo',
            'precio_max': 'Precio máximo',
            'ordering': 'Ordenar por: precio, -precio, fecha_creacion, -fecha_creacion, total_vendidos, -total_vendidos',
        },
        'ejemplos': {
            'buscar_camisetas': request.build_absolute_uri('/api/v1/productos/?search=camiseta'),
            'productos_por_marca': request.build_absolute_uri('/api/v1/productos/?marca=Nike'),
            'productos_baratos': request.build_absolute_uri('/api/v1/productos/?precio_max=50000'),
            'mas_vendidos': request.build_absolute_uri('/api/v1/productos/?ordering=-total_vendidos'),
        },
        'consumo_externo': {
            'descripcion': 'Esta API es pública y puede ser consumida por otros equipos',
            'formato': 'JSON',
            'autenticacion': 'No requiere (API pública)',
            'cors': 'Habilitado',
        }
    })


app_name = 'api'

urlpatterns = [
    # Endpoint raíz de la API
    path('', api_root, name='api-root'),

    # Incluir todas las rutas del router
    path('', include(router.urls)),
]
