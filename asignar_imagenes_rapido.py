"""
Script rápido para asignar imágenes placeholder a productos
Ejecutar: python manage.py shell < asignar_imagenes_rapido.py
"""

from tienda.models import Producto, ImagenProducto
from django.core.files.base import ContentFile
import requests
from io import BytesIO

def crear_imagen_placeholder(producto_id, nombre_producto, color='FF6B6B'):
    """Crear imagen placeholder desde una URL"""
    url = f'https://via.placeholder.com/400x500/{color}/FFFFFF?text={nombre_producto[:10]}'
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content, name=f'producto_{producto_id}.jpg')
    except Exception as e:
        print(f"Error descargando imagen para {nombre_producto}: {e}")
    return None

# Obtener primeros 5 productos
productos = Producto.objects.all()[:5]

colores = ['FF6B6B', '4ECDC4', '45B7D1', '96CEB4', 'FFEAA7']

print("Asignando imágenes de ejemplo...")

for i, producto in enumerate(productos):
    if not producto.imagen_principal:
        color = colores[i % len(colores)]
        imagen_content = crear_imagen_placeholder(producto.id, producto.nombre, color)
        
        if imagen_content:
            # Asignar imagen principal al producto
            producto.imagen_principal.save(
                f'producto_{producto.id}.jpg',
                imagen_content,
                save=True
            )
            print(f"✅ Imagen asignada a: {producto.nombre}")
        else:
            print(f"❌ No se pudo asignar imagen a: {producto.nombre}")
    else:
        print(f"⏭️  {producto.nombre} ya tiene imagen")

print("¡Proceso completado!")