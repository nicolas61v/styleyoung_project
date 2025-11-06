from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    imagen_principal = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'imagen_principal']
    
    def get_imagen_principal(self, obj):
        if obj.imagen_principal:
            request = self.context.get('request')
            url = obj.imagen_principal.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None