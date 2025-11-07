#!/bin/bash
# StyleYoung - AWS EC2 Setup Script
# Copia y pega esto en tu consola SSH de EC2
# IP: 52.73.136.81

echo "======================================"
echo "StyleYoung EC2 Setup"
echo "======================================"

# PASO 1: Actualizar sistema
echo "📦 Paso 1: Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# PASO 2: Instalar Docker
echo "🐳 Paso 2: Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# PASO 3: Añadir usuario ubuntu a grupo docker
echo "👤 Paso 3: Configurando usuario..."
sudo usermod -aG docker ubuntu

# PASO 4: Crear carpeta del proyecto
echo "📁 Paso 4: Creando carpeta..."
mkdir -p ~/styleyoung_project
cd ~/styleyoung_project

# PASO 5: Crear archivo .env
echo "⚙️  Paso 5: Creando archivo .env..."
cat > .env << 'EOF'
# Django
DEBUG=False
SECRET_KEY=tu-super-secret-key-aqui-cambialo-esto-es-importante
ALLOWED_HOSTS=52.73.136.81,yourdomain.tk

# AWS S3 (credenciales de AWS Academy)
USE_S3=True
AWS_ACCESS_KEY_ID=ASIA3EEVNO2FX4GEZFHH
AWS_SECRET_ACCESS_KEY=8rr4720tWAzEP9/akMF66zx3tSI98gH7Fd2Frcwi
AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEOb//////////wEaCXVzLXdlc3QtMiJHMEUCIATeHZKtVspKAQQlsyaFq6B/nKXyqH1eBc5unQtQWRAwAiEA5W2EhzQixejOamNFLXJMAT/kF7lz7beTNbu3417rRhQqrQIIr///////////ARAAGgw3NjQ4MTc1MzY2NTEiDBgiUVZ2prqAnfTjGiqBAsf/tV6ApcMfFpMkBTnlQ5aDdOV3BAopz7XoOO2AgS+FVkA0YmRHSsaXJ7O1vT0I11NC69yHn+XYNxh+sSGiI7WVX6kXWeSbETtPoj0qmHvYMJMTV35CmnM+0WgtXvTZbl3VZb8reSleConK/z9/RuTMHjBYAJ0tSFveGdo2tZSr/FidVx3LzkUwa6j+Smh6oxoVSpA0uTEfgz34RNLKzvF1ecb1vA/iQWyszi7D5+zrj/DjKwc27YGYf4xsh498aNG8eRSaHwhVLnmPekqFn7id6eWisiJqXAZ49nSnRuuvffe3aD28eMeA56eIwQM/f6U7adeIHGRaXsW1JvN2Hl7PMLGutMgGOp0BG9S1OePYKBDwQE24D7hq+/GnnTHWavLCuRFU3xtIS7NlsEFnjrUBmWjQ5IoAAE7e5p8z5F4j7rBC3RDBhPQzuHGWREQ7Ae2awQLN4OTvWBApVNabyjXb+Ikd38EMz14wkiQ/GoxKa0sWBaKHCqg8SyEy8CdUu8ru0KcYWvJGexjpKqeA6WJTRUofi0sEJ/Pk55HLHhdpOCe+N3wOUA==
AWS_STORAGE_BUCKET_NAME=styleyoung-productos
AWS_S3_REGION_NAME=us-east-1

# PostgreSQL
POSTGRES_DB=styleyoung
POSTGRES_USER=styleyoung_user
POSTGRES_PASSWORD=tu-postgres-password-super-segura-123

# Language
LANGUAGE_CODE=es
TIME_ZONE=America/Bogota
EOF

echo "✅ Archivo .env creado"

# PASO 6: Descargar imagen de Docker Hub
echo "⬇️  Paso 6: Descargando imagen de Docker Hub..."
docker pull nicolas61v/styleyoung:latest

# PASO 7: Ejecutar contenedor
echo "🚀 Paso 7: Ejecutando contenedor..."
docker run -d \
  --name styleyoung_app \
  --env-file .env \
  -p 80:8000 \
  nicolas61v/styleyoung:latest

# PASO 8: Verificar que está corriendo
echo "✅ Esperando a que inicie..."
sleep 5
docker ps

echo ""
echo "======================================"
echo "✅ SETUP COMPLETADO"
echo "======================================"
echo ""
echo "Tu aplicación está en:"
echo "http://52.73.136.81"
echo "http://52.73.136.81/admin"
echo "http://52.73.136.81/api/v1/productos/"
echo ""
echo "Ver logs:"
echo "docker logs -f styleyoung_app"
echo ""
echo "======================================"
