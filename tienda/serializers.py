from rest_framework import serializers
from .models import Producto, Categoria, Talla, ImagenProducto


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializador para la categoría"""
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class TallaSerializer(serializers.ModelSerializer):
    """Serializador para las tallas de productos"""
    class Meta:
        model = Talla
        fields = ['id', 'talla', 'stock']


class ImagenProductoSerializer(serializers.ModelSerializer):
    """Serializador para las imágenes adicionales de productos"""
    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'es_principal']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializador para productos con información anidada"""
    categoria = CategoriaSerializer(read_only=True)
    tallas = TallaSerializer(source='talla_set', many=True, read_only=True)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    imagen_principal_url = serializers.SerializerMethodField()
    stock_total = serializers.SerializerMethodField()

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
            'imagen_principal',
            'imagen_principal_url',
            'tallas',
            'imagenes',
            'stock_total',
            'total_vendidos',
            'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion', 'total_vendidos']

    def get_imagen_principal_url(self, obj):
        """Obtener la URL de la imagen principal"""
        request = self.context.get('request')
        imagen_url = obj.obtener_imagen_principal()
        if imagen_url and request is not None:
            return request.build_absolute_uri(imagen_url)
        return imagen_url

    def get_stock_total(self, obj):
        """Obtener el stock total del producto"""
        return obj.stock_total()