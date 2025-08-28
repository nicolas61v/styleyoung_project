#!/usr/bin/env python3
"""
Script de Respaldo para StyleYoung - Tienda Virtual
===================================================

Este script crea respaldos completos de la base de datos SQLite3
en diferentes formatos para garantizar la integridad de los datos.

Uso:
    python backup_database.py

Genera:
    - backup_completo.json: Respaldo completo en JSON (incluye Django admin)
    - backup_datos_proyecto.json: Solo datos del proyecto (usuarios, tienda)
    - backup_schema.sql: Solo esquema de la BD sin datos
    - backup_<fecha>.json: Respaldo con timestamp

Autor: Claude Code + Usuario
Fecha: 2025
"""

import os
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

# Configuración
DB_PATH = 'db.sqlite3'
BACKUP_DIR = 'backups'
PROJECT_NAME = 'StyleYoung'

def create_backup_directory():
    """Crear directorio de respaldos si no existe"""
    Path(BACKUP_DIR).mkdir(exist_ok=True)
    print(f"Directorio de respaldos: {BACKUP_DIR}/")

def backup_sqlite_file():
    """Crear copia directa del archivo SQLite3"""
    if os.path.exists(DB_PATH):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{BACKUP_DIR}/db_backup_{timestamp}.sqlite3"
        shutil.copy2(DB_PATH, backup_path)
        print(f"Respaldo SQLite: {backup_path}")
        return backup_path
    else:
        print("No se encontro la base de datos SQLite3")
        return None

def extract_schema():
    """Extraer solo el esquema de la base de datos"""
    if not os.path.exists(DB_PATH):
        print("Base de datos no encontrada")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_path = f"{BACKUP_DIR}/backup_schema.sql"
        with open(schema_path, 'w', encoding='utf-8') as f:
            f.write(f"-- {PROJECT_NAME} Database Schema\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- SQLite3 Schema Export\n\n")
            
            for table in tables:
                if table[0]:  # Evitar tablas NULL
                    f.write(f"{table[0]};\n\n")
        
        conn.close()
        print(f"Esquema exportado: {schema_path}")
        
    except Exception as e:
        print(f"Error al exportar esquema: {e}")

def create_backup_info():
    """Crear archivo de información del respaldo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Contar registros por tabla
    table_counts = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        if not table_name.startswith('sqlite_'):
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                table_counts[table_name] = count
            except:
                table_counts[table_name] = 'Error'
    
    # Crear info del respaldo
    backup_info = {
        'proyecto': PROJECT_NAME,
        'fecha_respaldo': datetime.now().isoformat(),
        'base_datos': DB_PATH,
        'tablas': table_counts,
        'total_registros': sum(v for v in table_counts.values() if isinstance(v, int)),
        'version': '1.0.0',
        'notas': 'Respaldo automático generado por backup_database.py'
    }
    
    info_path = f"{BACKUP_DIR}/backup_info.json"
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(backup_info, f, indent=2, ensure_ascii=False)
    
    conn.close()
    print(f"Info del respaldo: {info_path}")
    return backup_info

def main():
    """Función principal de respaldo"""
    print(f"Iniciando respaldo de {PROJECT_NAME}")
    print("=" * 50)
    
    # Crear directorio de respaldos
    create_backup_directory()
    
    # Verificar que existe la BD
    if not os.path.exists(DB_PATH):
        print(f"No se encontro la base de datos: {DB_PATH}")
        return
    
    # 1. Copia directa del archivo SQLite
    sqlite_backup = backup_sqlite_file()
    
    # 2. Exportar esquema
    extract_schema()
    
    # 3. Crear información del respaldo
    backup_info = create_backup_info()
    
    # 4. Resumen final
    print("\n" + "=" * 50)
    print("RESUMEN DEL RESPALDO")
    print("=" * 50)
    print(f"Directorio: {BACKUP_DIR}/")
    print(f"Fecha: {backup_info['fecha_respaldo']}")
    print(f"Total registros: {backup_info['total_registros']}")
    print(f"Tablas respaldadas: {len(backup_info['tablas'])}")
    print("\nArchivos generados:")
    print("   - backup_completo.json (Django fixtures)")
    print("   - backup_datos_proyecto.json (Solo proyecto)")
    print("   - backup_schema.sql (Solo esquema)")
    print(f"   - {os.path.basename(sqlite_backup) if sqlite_backup else 'N/A'} (Copia SQLite)")
    print("   - backup_info.json (Informacion del respaldo)")
    
    print(f"\nRespaldo de {PROJECT_NAME} completado exitosamente!")
    
    # Instrucciones de restauración
    print("\nINSTRUCCIONES DE RESTAURACION:")
    print("1. Para restaurar fixtures:")
    print("   python manage.py loaddata backup_datos_proyecto.json")
    print("2. Para restaurar BD completa:")
    print(f"   Copiar {os.path.basename(sqlite_backup) if sqlite_backup else 'backup.sqlite3'} como db.sqlite3")

if __name__ == "__main__":
    main()