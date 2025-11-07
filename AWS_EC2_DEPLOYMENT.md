# 🚀 Guía de Despliegue en AWS EC2

## StyleYoung - Tienda Virtual

Esta guía te ayudará a desplegar la aplicación StyleYoung en una instancia de AWS EC2 usando Docker.

---

## 📋 Requisitos Previos

1. **Cuenta AWS**: Tienes acceso a AWS Academy o una cuenta personal
2. **Acceso SSH**: Tienes las claves `.pem` para conectarte a la instancia
3. **Variables de entorno**: Credenciales de AWS S3 configuradas
4. **Dominio (opcional)**: Dominio .tk registrado en [dot.tk](http://www.dot.tk/)

---

## 🔧 PASO 1: Crear Instancia EC2

### 1.1 Acceder a AWS Console
- Ve a [AWS Console](https://console.aws.amazon.com/)
- Busca "EC2" → Click en "Lanzar instancia"

### 1.2 Configuración de la Instancia

**AMI (Sistema Operativo):**
- Selecciona: **Ubuntu 22.04 LTS**

**Tipo de Instancia:**
- Selecciona: **t2.micro** (Elegible para Free Tier)

**Almacenamiento:**
- **30 GB** de almacenamiento (suficiente para la app + images)
- Tipo: **gp3**

**Grupo de Seguridad (Puertos):**
```
Entrada:
- SSH (22): Tu IP (ej: 1.2.3.4/32)
- HTTP (80): 0.0.0.0/0 (todos)
- HTTPS (443): 0.0.0.0/0 (todos, si tienes SSL)
- Puerto 8000: 0.0.0.0/0 (opcional, para Gunicorn)

Salida:
- Todos los puertos (regla por defecto)
```

**Pares de Claves:**
- Crear nueva clave: `styleyoung-key.pem`
- Descargar y guardar en carpeta segura

---

## 🔐 PASO 2: Conectarse a la Instancia

### 2.1 Obtener la IP Pública
En AWS Console → Instancias → Copia la "IP pública elástica"

### 2.2 Conectarse por SSH (Windows - PowerShell)
```powershell
# Cambiar permisos de la clave
icacls "C:\ruta\styleyoung-key.pem" /reset
icacls "C:\ruta\styleyoung-key.pem" /grant:r "$($env:USERNAME):(F)"
icacls "C:\ruta\styleyoung-key.pem" /inheritance:r

# Conectarse
ssh -i "C:\ruta\styleyoung-key.pem" ubuntu@tu-ip-publica
```

### 2.2 Conectarse por SSH (Mac/Linux)
```bash
chmod 400 ~/styleyoung-key.pem
ssh -i ~/styleyoung-key.pem ubuntu@tu-ip-publica
```

---

## 📦 PASO 3: Instalar Docker en EC2

Una vez conectado a la instancia EC2:

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Añadir usuario ubuntu a grupo docker
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version

# Logout y login para aplicar cambios de grupo
exit
# Reconectar con SSH
```

---

## 📂 PASO 4: Clonar Repositorio y Configurar

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/styleyoung_project.git
cd styleyoung_project

# Crear archivo .env con credenciales
nano .env
```

### Contenido de `.env`:
```
DEBUG=False
SECRET_KEY=tu-secret-key-super-seguro-aqui
ALLOWED_HOSTS=tu-ip-publica,yourdomain.tk

# AWS S3
USE_S3=True
AWS_ACCESS_KEY_ID=ASIA3EEVNO2FX4GEZFHH
AWS_SECRET_ACCESS_KEY=tu-aws-secret-key
AWS_SESSION_TOKEN=tu-aws-session-token
AWS_STORAGE_BUCKET_NAME=styleyoung-productos
AWS_S3_REGION_NAME=us-east-1

# PostgreSQL
POSTGRES_DB=styleyoung
POSTGRES_USER=styleyoung_user
POSTGRES_PASSWORD=tu-postgres-password-segura

# Language
LANGUAGE_CODE=es
TIME_ZONE=America/Bogota
```

Guardar: `Ctrl+X` → `Y` → `Enter`

---

## 🐳 PASO 5: Iniciar Contenedores con Docker Compose

```bash
# Construir imagen y iniciar servicios
docker-compose up -d

# Verificar que los contenedores están corriendo
docker ps

# Ver logs (para ver si hay errores)
docker-compose logs -f web
```

### Esperado:
```
styleyoung_web    - "gunicorn --bind 0.0.0.0:8000..."
styleyoung_db     - "postgres"
styleyoung_nginx  - "nginx"
```

---

## 🗄️ PASO 6: Inicializar Base de Datos

```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superuser (administrador)
docker-compose exec web python manage.py createsuperuser

# Ejemplo:
# Username: admin
# Email: admin@styleyoung.com
# Password: tu-contraseña-super-segura
```

---

## ✅ PASO 7: Verificar que la Aplicación Funciona

### Acceso a la aplicación:
```
http://tu-ip-publica
http://tu-ip-publica/admin
http://tu-ip-publica/api/v1/productos/
```

### Verificar logs:
```bash
# Ver logs en tiempo real
docker-compose logs -f web

# Ver solo errores
docker-compose logs --tail=50 web
```

---

## 🌐 PASO 8: Configurar Dominio .tk (Opcional pero Recomendado)

### 8.1 Registrar dominio en dot.tk

1. Ir a [dot.tk](http://www.dot.tk/)
2. Buscar dominio deseado (ej: `styleyoung.tk`)
3. Seleccionar "Free"
4. Ingresar email y contraseña
5. Confirmar

### 8.2 Configurar DNS

En dot.tk Management → Manage DNS:

```
Type: A
Name: @ (o dejar en blanco)
Value: tu-ip-publica-de-ec2
TTL: 3600
```

### 8.3 Actualizar ALLOWED_HOSTS

```bash
# Editar .env
nano .env

# Cambiar ALLOWED_HOSTS:
ALLOWED_HOSTS=tu-ip-publica,styleyoung.tk,www.styleyoung.tk

# Reiniciar contenedores
docker-compose restart web
```

---

## 🔄 PASO 9: Mantener Actualizada la Aplicación

### Actualizar código:
```bash
cd styleyoung_project

# Traer cambios del repositorio
git pull origin main

# Reconstruir imagen si hay cambios en requirements.txt
docker-compose build --no-cache

# Reiniciar servicios
docker-compose down
docker-compose up -d
```

### Ver cambios en tiempo real:
```bash
docker-compose logs -f web
```

---

## 🐛 Troubleshooting (Solución de Problemas)

### Problema: "Permission denied" con Docker
```bash
# Solución:
sudo usermod -aG docker $USER
newgrp docker
```

### Problema: Puerto 8000 ya en uso
```bash
# Buscar qué está usando el puerto
sudo lsof -i :8000

# Matar proceso
sudo kill -9 PID
```

### Problema: Base de datos no conecta
```bash
# Verificar que el contenedor db está corriendo
docker ps | grep postgres

# Reiniciar base de datos
docker-compose restart db
docker-compose exec web python manage.py migrate
```

### Problema: Imágenes no suben a S3
```bash
# Verificar credenciales AWS en .env
# Verificar que USE_S3=True
# Revisar logs
docker-compose logs web | grep -i s3
```

---

## 📊 Monitoreo Básico

```bash
# Ver uso de recursos
docker stats

# Ver logs históricos (últimas 100 líneas)
docker-compose logs --tail=100 web

# Ver tamaño de volúmenes
docker volume ls

# Limpiar contenedores/imágenes sin usar
docker system prune -a
```

---

## 🛡️ Seguridad Recomendada

1. **Cambiar SECRET_KEY**: Generar una nueva en `https://miniwebtool.com/django-secret-key-generator/`
2. **HTTPS**: Usar Let's Encrypt + Certbot
3. **Firewalls**: AWS Security Groups bien configurados
4. **Actualizaciones**: Ejecutar `apt update && apt upgrade` regularmente
5. **Backups**: Hacer backup de la base de datos periódicamente

---

## 📝 Comandos Útiles

```bash
# Ver estado de todos los servicios
docker-compose ps

# Entrar en shell de Django
docker-compose exec web bash

# Ejecutar comando Django
docker-compose exec web python manage.py [comando]

# Ver variables de entorno en contenedor
docker-compose exec web env

# Reiniciar todos los servicios
docker-compose restart

# Detener todo sin borrar volúmenes
docker-compose down

# Detener y borrar TODO (¡cuidado!)
docker-compose down -v
```

---

## 📞 Contacto y Soporte

- **Repositorio**: https://github.com/tu-usuario/styleyoung_project
- **Docente**: Entrega antes de la fecha límite
- **Documentación Docker**: https://docs.docker.com/

---

**¡Éxito con el despliegue!** 🎉
