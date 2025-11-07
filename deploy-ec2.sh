#!/bin/bash

# Script para desplegar StyleYoung en EC2 con volumen persistente
# IMPORTANTE: Este script NO ejecuta migraciones automáticamente
# para preservar los datos existentes
#
# Uso:
#   Primera vez: ./deploy-ec2.sh --init
#   Actualizaciones: ./deploy-ec2.sh

set -e

echo "🚀 StyleYoung - EC2 Deployment Script"
echo "======================================"

# Variables
CONTAINER_NAME="styleyoung_app"
IMAGE_NAME="nicolas61v/styleyoung:latest"
VOLUME_NAME="styleyoung_data"
PORT="80:8000"
ENV_FILE=".env"

# PASO 1: Detener contenedor (SIN eliminar)
echo "⏹️  Deteniendo contenedor anterior..."
docker stop $CONTAINER_NAME 2>/dev/null || true

# PASO 2: Crear volumen si no existe
echo "📦 Creando volumen persistente..."
docker volume create $VOLUME_NAME 2>/dev/null || true

# PASO 3: Descargar imagen más reciente
echo "⬇️  Descargando imagen de Docker Hub..."
docker pull $IMAGE_NAME

# PASO 4: Eliminar SOLO el contenedor (el volumen se mantiene)
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

# PASO 6: Opción para inicializar (SOLO en la primera vez)
if [[ "$1" == "--init" ]]; then
    echo "🔄 INICIALIZANDO: Ejecutando migraciones..."
    docker exec $CONTAINER_NAME python manage.py migrate
    echo "✅ Migraciones completadas"
else
    echo "⚠️  NOTA: Saltando migraciones (datos preservados)"
    echo "   Si es la PRIMERA vez, ejecuta: ./deploy-ec2.sh --init"
fi

# PASO 7: Compilar traducciones
echo "🌍 Compilando traducciones..."
docker exec $CONTAINER_NAME python manage.py compilemessages || true

# PASO 8: Ver logs
echo "📊 Últimos logs:"
docker logs --tail=20 $CONTAINER_NAME

echo ""
echo "✅ ¡Despliegue completado!"
echo "======================================"
echo "Aplicación disponible en:"
echo "  - http://52.73.136.81"
echo "  - http://107.21.166.51"
echo ""
echo "Admin en:"
echo "  - http://52.73.136.81/admin-panel/"
echo ""
echo "Comandos útiles:"
echo "  docker logs -f $CONTAINER_NAME     # Ver logs en tiempo real"
echo "  docker restart $CONTAINER_NAME     # Reiniciar (datos persisten)"
echo "  docker ps                          # Ver contenedores"
echo "  ./deploy-ec2.sh --init             # Inicializar BD (PRIMERA VEZ SOLO)"
echo ""
