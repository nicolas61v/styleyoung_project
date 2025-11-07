#!/bin/bash

# Script para desplegar StyleYoung en EC2 con volumen persistente
# Auto-detecta si necesita migraciones

set -e

echo "🚀 StyleYoung - EC2 Deployment Script"
echo "======================================"

# Variables
CONTAINER_NAME="styleyoung_app"
IMAGE_NAME="nicolas61v/styleyoung:latest"
VOLUME_NAME="styleyoung_data"
VOLUME_MEDIA="styleyoung_media"
PORT="80:8000"
ENV_FILE=".env"

# PASO 1: Detener contenedor
echo "⏹️  Deteniendo contenedor anterior..."
docker stop $CONTAINER_NAME 2>/dev/null || true

# PASO 2: Crear volúmenes si no existen
echo "📦 Creando volúmenes persistentes..."
docker volume create $VOLUME_NAME 2>/dev/null || true
docker volume create $VOLUME_MEDIA 2>/dev/null || true

# PASO 3: Descargar imagen más reciente
echo "⬇️  Descargando imagen de Docker Hub..."
docker pull $IMAGE_NAME

# PASO 4: Eliminar contenedor antiguo
echo "🗑️  Eliminando contenedor antiguo..."
docker rm $CONTAINER_NAME 2>/dev/null || true

# PASO 5: Ejecutar contenedor CON VOLÚMENES PERSISTENTES (DB + MEDIA)
echo "🐳 Iniciando contenedor con volúmenes persistentes..."
docker run -d \
  --name $CONTAINER_NAME \
  --env-file $ENV_FILE \
  -p $PORT \
  -v $VOLUME_NAME:/app/db \
  -v $VOLUME_MEDIA:/app/media \
  $IMAGE_NAME

echo "⏳ Esperando a que el contenedor inicie..."
sleep 5

# PASO 6: Ejecutar migrations (siempre, Django es inteligente)
# Django solo aplicará las migraciones que falten
echo "🔄 Sincronizando base de datos..."
docker exec $CONTAINER_NAME python manage.py migrate

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
