"""
Script para asignar imágenes a productos existentes
Ejecutar desde el shell de Django: python manage.py shell
Luego: exec(open('asignar_imagenes_ejemplo.py').read())
"""

from tienda.models import Producto, ImagenProducto
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from urllib.parse import urlparse
import os

def descargar_imagen_desde_url(url, nombre_archivo):
    """Descargar imagen desde URL y guardarla"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Crear archivo temporal
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(response.content)
        temp_file.flush()
        
        return temp_file.name
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return None

def asignar_imagenes_ejemplo():
    """Asignar imágenes de ejemplo a productos existentes"""
    
    # URLs de imágenes de ejemplo (usar URLs reales o locales)
    imagenes_ejemplo = {
        'ropa': [
            'https://via.placeholder.com/300x400/FF6B6B/FFFFFF?text=Camiseta',
            'https://via.placeholder.com/300x400/4ECDC4/FFFFFF?text=Pantalon',
            'https://via.placeholder.com/300x400/45B7D1/FFFFFF?text=Chaqueta',
            'https://via.placeholder.com/300x400/96CEB4/FFFFFF?text=Vestido',
            'https://via.placeholder.com/300x400/FFEAA7/000000?text=Blusa',
        ]
    }
    
    productos = Producto.objects.all()[:5]  # Primeros 5 productos
    
    print(f"Asignando imágenes a {productos.count()} productos...")
    
    for i, producto in enumerate(productos):
        url_imagen = imagenes_ejemplo['ropa'][i % len(imagenes_ejemplo['ropa'])]
        
        # Descargar imagen
        archivo_temp = descargar_imagen_desde_url(url_imagen, f'producto_{producto.id}.jpg')
        
        if archivo_temp:
            # Crear registro de imagen
            with open(archivo_temp, 'rb') as f:
                imagen_producto = ImagenProducto.objects.create(
                    producto=producto,
                    descripcion=f'Imagen principal de {producto.nombre}',
                    es_principal=True,
                    orden=1
                )
                
                # Asignar archivo
                imagen_producto.imagen.save(
                    f'producto_{producto.id}_{i}.jpg',
                    File(f),
                    save=True
                )
                
            # Limpiar archivo temporal
            os.unlink(archivo_temp)
            print(f"✅ Imagen asignada a: {producto.nombre}")
        else:
            print(f"❌ No se pudo asignar imagen a: {producto.nombre}")

def asignar_imagenes_locales():
    """Método alternativo usando imágenes locales"""
    
    # Directorio con imágenes locales (crear esta carpeta y poner imágenes)
    directorio_imagenes = 'imagenes_productos/'
    
    if not os.path.exists(directorio_imagenes):
        print(f"Crear directorio '{directorio_imagenes}' y añadir imágenes .jpg")
        return
    
    productos = Producto.objects.all()
    archivos_imagen = [f for f in os.listdir(directorio_imagenes) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Encontradas {len(archivos_imagen)} imágenes para {productos.count()} productos")
    
    for i, producto in enumerate(productos):
        if i < len(archivos_imagen):
            ruta_imagen = os.path.join(directorio_imagenes, archivos_imagen[i])
            
            with open(ruta_imagen, 'rb') as f:
                imagen_producto = ImagenProducto.objects.create(
                    producto=producto,
                    descripcion=f'Imagen de {producto.nombre}',
                    es_principal=True,
                    orden=1
                )
                
                imagen_producto.imagen.save(
                    f'producto_{producto.id}_{archivos_imagen[i]}',
                    File(f),
                    save=True
                )
                
            print(f"✅ Imagen local asignada a: {producto.nombre}")

def crear_productos_con_imagenes():
    """Crear productos de ejemplo con imágenes"""
    from tienda.models import Categoria
    
    # Crear categoría si no existe
    categoria, created = Categoria.objects.get_or_create(
        nombre='Ropa Casual',
        defaults={'descripcion': 'Ropa para uso diario'}
    )
    
    productos_ejemplo = [
        {'nombre': 'Camiseta Básica', 'precio': 25.99, 'marca': 'StyleYoung', 'color': 'Blanco'},
        {'nombre': 'Jeans Clásicos', 'precio': 79.99, 'marca': 'StyleYoung', 'color': 'Azul'},
        {'nombre': 'Chaqueta Deportiva', 'precio': 129.99, 'marca': 'StyleYoung', 'color': 'Negro'},
    ]
    
    for datos in productos_ejemplo:
        producto, created = Producto.objects.get_or_create(
            nombre=datos['nombre'],
            defaults={
                'descripcion': f'Descripción de {datos["nombre"]}',
                'precio': datos['precio'],
                'marca': datos['marca'],
                'color': datos['color'],
                'material': 'Algodón',
                'categoria': categoria
            }
        )
        
        if created:
            print(f"✅ Producto creado: {producto.nombre}")

# Ejecutar las funciones
print("=== ASIGNACIÓN DE IMÁGENES A PRODUCTOS ===")
print("Opciones disponibles:")
print("1. asignar_imagenes_ejemplo() - Descarga imágenes desde URLs")
print("2. asignar_imagenes_locales() - Usa imágenes locales")
print("3. crear_productos_con_imagenes() - Crea productos de ejemplo")

# Descomentar la función que quieras ejecutar:
# asignar_imagenes_ejemplo()
# asignar_imagenes_locales()
# crear_productos_con_imagenes()

print("\nPara ejecutar, descomentar la función deseada y ejecutar el script")
print("Ejemplo: python manage.py shell")
print(">>> exec(open('asignar_imagenes_ejemplo.py').read())")