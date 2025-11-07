#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de depuración para la creación de productos
Usalo asi: python debug_producto.py
"""

import os
import django
import logging

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'styleyoung_project.settings')
django.setup()

from tienda.models import Producto, Categoria, Talla
from tienda.forms import ProductoForm, TallaFormSet
from django.test import RequestFactory
from decimal import Decimal

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("\n" + "="*80)
print("DEBUG: Creacion de Productos - StyleYoung")
print("="*80 + "\n")

# 1. Verificar categorías
print("[1] VERIFICANDO CATEGORIAS...")
categorias = Categoria.objects.all()
print(f"    Total de categorias: {categorias.count()}")
for cat in categorias:
    print(f"    - {cat.nombre}")

if not categorias.exists():
    print("    [ERROR] No hay categorias. Creando una por defecto...")
    cat = Categoria.objects.create(nombre="Default", descripcion="Categoria por defecto")
    print(f"    [OK] Categoria creada: {cat.nombre}")

# 2. Test del formulario de producto
print("\n[2] PROBANDO FORMULARIO DE PRODUCTO...")
test_data = {
    'nombre': 'Producto Test',
    'descripcion': 'Test description',
    'precio': '99.99',
    'marca': 'TestMarca',
    'color': 'Rojo',
    'material': 'Algodon',
    'categoria': categorias.first().id,
}

form = ProductoForm(test_data)
print(f"    Form valido: {form.is_valid()}")
if not form.is_valid():
    print(f"    [ERROR] Errores: {form.errors}")
else:
    print(f"    [OK] Formulario valido")

# 3. Test del formset de tallas
print("\n[3] PROBANDO FORMSET DE TALLAS...")
# IMPORTANTE: El prefijo DEBE ser 'talla_set' que es el prefijo en la vista
# El management form NECESITA estos campos
formset_data = {
    'talla_set-TOTAL_FORMS': '5',
    'talla_set-INITIAL_FORMS': '0',
    'talla_set-MIN_NUM_FORMS': '0',
    'talla_set-MAX_NUM_FORMS': '1000',
    # Fila 0: M con stock 10
    'talla_set-0-talla': 'M',
    'talla_set-0-stock': '10',
    'talla_set-0-id': '',  # ID vacío para nuevo
    'talla_set-0-DELETE': '',
    # Filas 1-4: vacías
    'talla_set-1-talla': '',
    'talla_set-1-stock': '',
    'talla_set-1-id': '',
    'talla_set-1-DELETE': '',
    'talla_set-2-talla': '',
    'talla_set-2-stock': '',
    'talla_set-2-id': '',
    'talla_set-2-DELETE': '',
    'talla_set-3-talla': '',
    'talla_set-3-stock': '',
    'talla_set-3-id': '',
    'talla_set-3-DELETE': '',
    'talla_set-4-talla': '',
    'talla_set-4-stock': '',
    'talla_set-4-id': '',
    'talla_set-4-DELETE': '',
}

formset = TallaFormSet(formset_data, queryset=Talla.objects.none(), prefix='talla_set')
print(f"    Formset valido: {formset.is_valid()}")
if not formset.is_valid():
    print(f"    [ERROR] Errores formset: {formset.errors}")
    print(f"    [ERROR] Non-form errors: {formset.non_form_errors()}")
else:
    print(f"    [OK] Formset valido")

    # Contar tallas válidas
    tallas_validas = 0
    for idx, form_talla in enumerate(formset):
        if form_talla.cleaned_data and not form_talla.cleaned_data.get('DELETE'):
            if form_talla.cleaned_data.get('talla'):
                tallas_validas += 1
                print(f"    - Talla {idx} valida: {form_talla.cleaned_data.get('talla')}")

    print(f"    Total de tallas validas: {tallas_validas}")

# 4. Test de creación completa
print("\n[4] PROBANDO CREACION COMPLETA DE PRODUCTO...")
combined_data = {**test_data, **formset_data}

form_completo = ProductoForm(combined_data)
formset_completo = TallaFormSet(combined_data, queryset=Talla.objects.none(), prefix='talla_set')

print(f"    Formulario valido: {form_completo.is_valid()}")
print(f"    Formset valido: {formset_completo.is_valid()}")

if form_completo.is_valid() and formset_completo.is_valid():
    print("\n    [OK] AMBOS FORMULARIOS SON VALIDOS")
    print("    Procediendo a guardar...")

    producto = form_completo.save()
    print(f"    [OK] Producto guardado: {producto.id} - {producto.nombre}")

    for form_talla in formset_completo:
        if form_talla.cleaned_data and not form_talla.cleaned_data.get('DELETE'):
            if form_talla.cleaned_data.get('talla'):
                talla = form_talla.save(commit=False)
                talla.producto = producto
                talla.save()
                print(f"    [OK] Talla guardada: {talla.talla} (Stock: {talla.stock})")

    print(f"\n    Stock total del producto: {producto.stock_total()}")
    print("    [OK] PRODUCTO CREADO CON EXITO")
else:
    print(f"\n    [ERROR] ERROR EN LOS FORMULARIOS")
    if not form_completo.is_valid():
        print(f"    Errores del formulario: {form_completo.errors}")
    if not formset_completo.is_valid():
        print(f"    Errores del formset: {formset_completo.errors}")

print("\n" + "="*80)
print("DEBUG COMPLETADO")
print("="*80 + "\n")
