"""
API Views para StyleYoung - API REST completa

Esta API permite que otros equipos consuman nuestros productos
y también la usamos nosotros mismos para demostrar que funciona
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producto, Categoria
from .serializers import (
    ProductoSerializer,
    ProductoListSerializer,
    CategoriaSerializer
)


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet para Productos

    Endpoints disponibles:
    - GET /api/v1/productos/ - Lista todos los productos
    - GET /api/v1/productos/{id}/ - Detalle de un producto
    - GET /api/v1/productos/en-stock/ - Solo productos con stock
    - GET /api/v1/productos/?search=... - Búsqueda de productos

    Filtros disponibles:
    - categoria (ID)
    - marca
    - color
    - precio_min, precio_max
    """

    queryset = Producto.objects.all().select_related('categoria').prefetch_related('tallas', 'imagenes')
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'marca', 'descripcion', 'color', 'material']
    ordering_fields = ['precio', 'fecha_creacion', 'total_vendidos']
    ordering = ['-fecha_creacion']

    def get_serializer_class(self):
        """
        Usar serializer simplificado para listados,
        completo para detalle
        """
        if self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer

    def get_queryset(self):
        """
        Filtros personalizados via query params
        """
        queryset = super().get_queryset()

        # Filtro por categoría
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        # Filtro por marca
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(marca__iexact=marca)

        # Filtro por color
        color = self.request.query_params.get('color', None)
        if color:
            queryset = queryset.filter(color__iexact=color)

        # Filtro por rango de precio
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)

        return queryset

    @action(detail=False, methods=['get'])
    def en_stock(self, request):
        """
        Endpoint personalizado: /api/v1/productos/en-stock/

        Retorna solo productos que tienen stock disponible
        """
        # Obtener productos que tienen al menos una talla con stock
        productos_con_stock = self.queryset.filter(
            talla__stock__gt=0
        ).distinct()

        page = self.paginate_queryset(productos_con_stock)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(productos_con_stock, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def mas_vendidos(self, request):
        """
        Endpoint personalizado: /api/v1/productos/mas-vendidos/

        Retorna los productos más vendidos
        """
        top_productos = self.queryset.order_by('-total_vendidos')[:10]

        serializer = self.get_serializer(top_productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint personalizado: /api/v1/productos/estadisticas/

        Retorna estadísticas generales de productos
        """
        total_productos = self.queryset.count()
        productos_con_stock = self.queryset.filter(talla__stock__gt=0).distinct().count()
        total_vendidos = sum(p.total_vendidos for p in self.queryset)

        stats = {
            'total_productos': total_productos,
            'productos_disponibles': productos_con_stock,
            'productos_agotados': total_productos - productos_con_stock,
            'total_ventas': total_vendidos,
            'categorias_activas': Categoria.objects.count()
        }

        return Response(stats)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet para Categorías

    Endpoints disponibles:
    - GET /api/v1/categorias/ - Lista todas las categorías
    - GET /api/v1/categorias/{id}/ - Detalle de una categoría
    - GET /api/v1/categorias/{id}/productos/ - Productos de una categoría
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """
        Endpoint: /api/v1/categorias/{id}/productos/

        Retorna todos los productos de una categoría específica
        """
        categoria = self.get_object()
        productos = categoria.producto_set.all()

        page = self.paginate_queryset(productos)
        if page is not None:
            serializer = ProductoListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductoListSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data)
