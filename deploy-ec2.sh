#!/bin/bash

# Script para desplegar StyleYoung en EC2 con volumen persistente
# El script automáticamente detecta si necesita hacer migraciones
# y preserva datos existentes

set -e

echo "🚀 StyleYoung - EC2 Deployment Script"
echo "======================================"

# Variables
CONTAINER_NAME="styleyoung_app"
IMAGE_NAME="nicolas61v/styleyoung:latest"
VOLUME_NAME="styleyoung_data"
PORT="80:8000"
ENV_FILE=".env"

# PASO 1: Detener contenedor
echo "⏹️  Deteniendo contenedor anterior..."
docker stop $CONTAINER_NAME 2>/dev/null || true

# PASO 2: Crear volumen si no existe
echo "📦 Creando volumen persistente..."
docker volume create $VOLUME_NAME 2>/dev/null || true

# PASO 3: Descargar imagen más reciente
echo "⬇️  Descargando imagen de Docker Hub..."
docker pull $IMAGE_NAME

# PASO 4: Eliminar contenedor antiguo
echo "🗑️  Eliminando contenedor antiguo..."
docker rm $CONTAINER_NAME 2>/dev/null || true

# PASO 5: Ejecutar contenedor CON VOLUMEN
echo "🐳 Iniciando contenedor con volumen persistente..."
docker run -d \
  --name $CONTAINER_NAME \
  --env-file $ENV_FILE \
  -p $PORT \
  -v $VOLUME_NAME:/app/db \
  $IMAGE_NAME

echo "⏳ Esperando a que el contenedor inicie..."
sleep 5

# PASO 6: Detectar si necesita migraciones automáticamente
echo "🔍 Detectando estado de la base de datos..."
if docker exec $CONTAINER_NAME test -f /app/db/db.sqlite3; then
    echo "   ✅ Base de datos existente - saltando migraciones"
else
    echo "   ⚠️  Base de datos vacía - ejecutando migraciones..."
    docker exec $CONTAINER_NAME python manage.py migrate
    echo "   ✅ Migraciones completadas"
fi

# PASO 7: Compilar traducciones
echo "🌍 Compilando traducciones..."
docker exec $CONTAINER_NAME python manage.py compilemessages || true

# PASO 8: Ver logs
echo "📊 Últimos logs:"
docker logs --tail=10 $CONTAINER_NAME

echo ""
echo "✅ ¡Despliegue completado!"
echo "======================================"
echo "Comandos útiles:"
echo "  docker logs -f $CONTAINER_NAME     # Ver logs en tiempo real"
echo "  docker restart $CONTAINER_NAME     # Reiniciar (datos persisten)"
echo "  docker ps                          # Ver contenedores"
echo ""
