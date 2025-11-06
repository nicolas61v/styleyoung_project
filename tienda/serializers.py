"""
Serializers para la API REST de StyleYoung

Estos serializers convierten los modelos Django a JSON para la API
"""
from rest_framework import serializers
from .models import Producto, Categoria, Talla, ImagenProducto


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""

    total_productos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'total_productos']

    def get_total_productos(self, obj):
        """Obtener total de productos en la categoría"""
        return obj.producto_set.count()


class TallaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Talla"""

    class Meta:
        model = Talla
        fields = ['id', 'talla', 'stock']


class ImagenProductoSerializer(serializers.ModelSerializer):
    """Serializer para imágenes adicionales del producto"""

    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen_url', 'descripcion', 'es_principal', 'orden']

    def get_imagen_url(self, obj):
        """Obtener URL completa de la imagen"""
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        elif obj.imagen:
            return obj.imagen.url
        return None


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer completo para el modelo Producto

    Incluye toda la información necesaria para que otros equipos
    puedan consumir la API y mostrar los productos
    """

    categoria = CategoriaSerializer(read_only=True)
    tallas = TallaSerializer(many=True, read_only=True, source='talla_set')
    imagenes = ImagenProductoSerializer(many=True, read_only=True, source='imagenproducto_set')

    stock_total = serializers.SerializerMethodField()
    imagen_principal_url = serializers.SerializerMethodField()
    url_detalle = serializers.SerializerMethodField()
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'marca',
            'color',
            'material',
            'categoria',
            'imagen_principal_url',
            'imagenes',
            'tallas',
            'stock_total',
            'total_vendidos',
            'fecha_creacion',
            'url_detalle',
            'disponible'
        ]

    def get_stock_total(self, obj):
        """Calcular stock total del producto"""
        return obj.stock_total()

    def get_imagen_principal_url(self, obj):
        """Obtener URL completa de la imagen principal"""
        request = self.context.get('request')
        if obj.imagen_principal and request:
            return request.build_absolute_uri(obj.imagen_principal.url)
        elif obj.imagen_principal:
            return obj.imagen_principal.url
        return None

    def get_url_detalle(self, obj):
        """Obtener URL del detalle del producto"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/producto/{obj.id}/')
        return f'/producto/{obj.id}/'

    def get_disponible(self, obj):
        """Verificar si el producto está disponible"""
        return obj.stock_total() > 0


class ProductoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de productos
    (menos datos para mejorar performance)
    """

    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    stock_total = serializers.SerializerMethodField()
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'precio',
            'marca',
            'color',
            'categoria_nombre',
            'imagen_url',
            'stock_total',
            'total_vendidos'
        ]

    def get_stock_total(self, obj):
        return obj.stock_total()

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen_principal and request:
            return request.build_absolute_uri(obj.imagen_principal.url)
        elif obj.imagen_principal:
            return obj.imagen_principal.url
        return None
