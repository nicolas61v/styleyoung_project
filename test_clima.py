#!/usr/bin/env python
"""
Script para probar el servicio de clima
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'styleyoung_project.settings')
django.setup()

from tienda.services.clima_service import ClimaService

print("=" * 60)
print("Probando ClimaService...")
print("=" * 60)

# Limpiar cache para obtener datos frescos
from django.core.cache import cache
cache.clear()

clima = ClimaService.obtener_clima()

if clima:
    print("\nObtener clima correctamente:")
    print(f"  Ciudad: {clima.get('ciudad')}")
    print(f"  Temperatura: {clima.get('temperatura')}C")
    print(f"  Sensacion termica: {clima.get('sensacion_termica')}C")
    print(f"  Humedad: {clima.get('humedad')}%")
    print(f"  Descripcion: {clima.get('descripcion')}")
    print(f"  Icon URL: {clima.get('icon_url')}")
else:
    print("\nError: No se pudo obtener el clima")
    print("  Verifica la conexion a internet y la API key")

print("\n" + "=" * 60)
