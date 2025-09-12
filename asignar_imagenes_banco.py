#!/usr/bin/env python
"""
Script para asignar imágenes del bancoImagenes a los productos
Ejecutar: python manage.py shell < asignar_imagenes_banco.py
"""

import os
import shutil
from tienda.models import Producto
from django.core.files.base import ContentFile

# Mapeo de productos con sus imágenes correspondientes
MAPEO_IMAGENES = {
    "Blusa Casual Azul": "Blusa Casual Azul.jpg",
    "Jean Skinny Negro": "Jean Skinny Negro.jpg", 
    "Vestido Floral Primavera": "Vestido Floral Primavera.jpg",
    "Blusa Blanca Elegante": "Blusa Blanca Elegante.jpg",
    "Leggings Deportivos": "Leggings Deportivos.jpg",
    "Vestido Rojo Fiesta": "Vestido Rojo Fiesta.jpg",
    "Collar Dorado Moderno": "Collar Dorado Moderno.jpg",
    "Chaqueta de Mezclilla": "Chaqueta de Mezclilla.jpg",
    "Blusa Rosa Romántica": "Blusa Rosa Romántica.jpg",
    "Pantalón Formal Gris": "Pantalón Formal Gris.jpg",
    "Vestido Negro Básico": "Vestido Negro Básico.jpg",
    "Bolso Crossbody Camel": "Bolso Crossbody Camel.jpg",
    "Blazer Negro Ejecutivo": "Blazer Negro Ejecutivo.jpg",
    "Blusa Verde Esmeralda": "Blusa Verde Esmeralda.jpg",
    "Jean de Tiro Alto": "Jean de Tiro Alto.jpg",
    "Vestido Midi Lunares": "Vestido Midi Lunares.jpg",
    "Aretes Plateados Largos": "Aretes plaetados.jpg",  # Nota: hay un typo en el archivo
    "Cardigan Oversized Beige": "Cardigan oversize beige.jpg",
    "Crop Top Estampado": "CropTop estampado.jpg",
    "Pantalón Palazzo Negro": "pantalon palazzo.jpg"
}

def asignar_imagenes():
    """Asignar imágenes a productos desde bancoImagenes"""
    banco_dir = "./bancoImagenes"
    media_dir = "./media/productos"
    
    # Crear directorio media/productos si no existe
    os.makedirs(media_dir, exist_ok=True)
    
    productos_actualizados = 0
    productos_no_encontrados = []
    imagenes_no_encontradas = []
    
    print("🚀 Iniciando asignación de imágenes...")
    print("=" * 50)
    
    for producto in Producto.objects.all():
        nombre_producto = producto.nombre
        
        # Buscar imagen correspondiente
        if nombre_producto in MAPEO_IMAGENES:
            nombre_imagen = MAPEO_IMAGENES[nombre_producto]
            ruta_origen = os.path.join(banco_dir, nombre_imagen)
            
            if os.path.exists(ruta_origen):
                try:
                    # Leer el archivo de imagen
                    with open(ruta_origen, 'rb') as f:
                        contenido_imagen = f.read()
                    
                    # Crear nombre limpio para el archivo
                    nombre_archivo_limpio = f"producto_{producto.id}_{nombre_imagen.replace(' ', '_')}"
                    
                    # Asignar al campo imagen_principal
                    producto.imagen_principal.save(
                        nombre_archivo_limpio,
                        ContentFile(contenido_imagen),
                        save=True
                    )
                    
                    productos_actualizados += 1
                    print(f"✅ {producto.id:2d}. {nombre_producto:<30} → {nombre_imagen}")
                    
                except Exception as e:
                    print(f"❌ Error asignando imagen a {nombre_producto}: {e}")
            else:
                imagenes_no_encontradas.append(f"{nombre_producto} → {nombre_imagen}")
                print(f"🔍 Imagen no encontrada: {nombre_imagen}")
        else:
            productos_no_encontrados.append(nombre_producto)
            print(f"⚠️  No se encontró mapeo para: {nombre_producto}")
    
    print("=" * 50)
    print(f"📊 RESUMEN:")
    print(f"✅ Productos actualizados: {productos_actualizados}")
    print(f"⚠️  Productos sin mapeo: {len(productos_no_encontrados)}")
    print(f"🔍 Imágenes no encontradas: {len(imagenes_no_encontradas)}")
    
    if productos_no_encontrados:
        print(f"\n📝 Productos sin mapeo:")
        for producto in productos_no_encontrados:
            print(f"   - {producto}")
    
    if imagenes_no_encontradas:
        print(f"\n🔍 Imágenes no encontradas:")
        for item in imagenes_no_encontradas:
            print(f"   - {item}")
    
    print("\n🎉 ¡Proceso completado!")

# Ejecutar el script
if __name__ == "__main__":
    asignar_imagenes()
else:
    asignar_imagenes()