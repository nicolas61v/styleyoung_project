# 🐳 Despliegue StyleYoung en AWS EC2 usando Docker Hub + GitHub Actions

## Arquitectura

```
Tu Computadora (Git Push)    GitHub Actions         Docker Hub           AWS EC2
         ↓                           ↓                  ↓                    ↓
    git push            →   Construye imagen   →  Sube imagen    →   Descarga y ejecuta
                            automáticamente        automáticamente       (docker pull + run)
```

**SIN NECESIDAD DE DOCKER EN TU PC** ✨

---

## 📋 PARTE 1: Configurar GitHub Actions (Una sola vez)

### 1.1 Crear Cuenta Docker Hub

1. Ve a https://hub.docker.com/
2. Click en "Sign Up"
3. Crea tu cuenta (ej: `tu-usuario`)
4. Confirma email

### 1.2 Crear Token en Docker Hub

1. Ve a https://hub.docker.com/settings/security
2. Click en "New Access Token"
3. Nombre: `github-actions`
4. Copia el token completo (lo necesitarás en GitHub)

### 1.3 Crear Secretos en GitHub

1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click en **"New repository secret"**

**Crear Secreto 1:**
- Name: `DOCKER_USERNAME`
- Value: `nicolas61v` (tu usuario de Docker Hub)

**Crear Secreto 2:**
- Name: `DOCKER_PASSWORD`
- Value: El token que copiaste en 1.2

### 1.4 Verificar Workflow de GitHub Actions

El archivo `.github/workflows/docker-build-push.yml` ya está creado.

Este archivo automáticamente:
- ✅ Se ejecuta cuando haces push a `main`
- ✅ Construye la imagen Docker
- ✅ La sube a Docker Hub
- ✅ **Todo sin que hagas nada en tu PC**

Puedes verificar el progreso en:
```
https://github.com/tu-usuario/styleyoung_project/actions
```

---

## ✨ PARTE 2: Tu Flujo de Trabajo (Super Simple)

### Cada vez que hagas cambios:

```bash
# 1. Navega al proyecto
cd C:\Users\dejavu\Documents\NicolasINgenieroNASA\styleyoung_project

# 2. Agregar cambios
git add .

# 3. Commit
git commit -m "Descripción de tus cambios"

# 4. Push a GitHub
git push origin main
```

**¡Eso es TODO!** GitHub Actions automáticamente:
- Construye la imagen
- La sube a Docker Hub
- La deja lista para tu EC2

**Verifica el progreso** visitando:
```
https://github.com/tu-usuario/styleyoung_project/actions
```

---

## 🖥️ PARTE 3: Configurar AWS EC2 (Una sola vez)

### 3.1 Conectarse a EC2

```bash
ssh -i "C:\ruta\styleyoung-key.pem" ubuntu@52.73.136.81
```

### 3.2 Instalar Docker en EC2

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Añadir usuario ubuntu a grupo docker
sudo usermod -aG docker ubuntu

# Logout y reconectar
exit
```

Reconecta con SSH.

### 3.3 Crear Carpeta del Proyecto

```bash
mkdir -p ~/styleyoung_project
cd ~/styleyoung_project
```

### 3.4 Crear archivo `.env`

```bash
nano .env
```

Copia y pega esto **(MODIFICA LAS CREDENCIALES):**

```
# Django
DEBUG=False
SECRET_KEY=tu-super-secret-key-aqui-cambialo
ALLOWED_HOSTS=52.73.136.81,yourdomain.tk

# AWS S3
USE_S3=True
AWS_ACCESS_KEY_ID=TU_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=TU_SECRET_KEY
AWS_SESSION_TOKEN=TU_SESSION_TOKEN
AWS_STORAGE_BUCKET_NAME=styleyoung-productos
AWS_S3_REGION_NAME=us-east-1

# PostgreSQL
POSTGRES_DB=styleyoung
POSTGRES_USER=styleyoung_user
POSTGRES_PASSWORD=tu-postgres-password

# Language
LANGUAGE_CODE=es
TIME_ZONE=America/Bogota
```

Guardar: `Ctrl+X` → `Y` → `Enter`

---

## 🐳 PARTE 4: Ejecutar Contenedor en EC2

### 4.1 Descargar Imagen de Docker Hub

```bash
# Reemplaza "tu-usuario" con tu usuario de Docker Hub
docker pull tu-usuario/styleyoung:latest

# Ejemplo:
docker pull nicolasjengienereonasa/styleyoung:latest
```

### 4.2 Ejecutar Contenedor

```bash
docker run -d \
  --name styleyoung_app \
  --env-file .env \
  -p 80:8000 \
  tu-usuario/styleyoung:latest
```

### 4.3 Verificar que está Corriendo

```bash
docker ps
```

Deberías ver tu contenedor listado.

### 4.4 Ver Logs

```bash
docker logs -f styleyoung_app
```

Deberías ver algo como:
```
[INFO] Starting gunicorn
[INFO] Booting worker with pid: 8
```

---

## ✅ PARTE 5: Acceder a la Aplicación

Abre tu navegador en:

```
http://52.73.136.81
http://52.73.136.81/admin
http://52.73.136.81/api/v1/productos/
```

---

## 🔄 PARTE 6: Actualizar Cuando Hagas Cambios

**En tu computadora:**

```bash
git add .
git commit -m "Tus cambios"
git push origin main
```

**GitHub Actions** automáticamente:
1. Construye la nueva imagen
2. La sube a Docker Hub

**En EC2:**

```bash
# Esperar a que GitHub Actions termine
# Luego ejecutar:

docker stop styleyoung_app
docker rm styleyoung_app
docker pull tu-usuario/styleyoung:latest
docker run -d \
  --name styleyoung_app \
  --env-file .env \
  -p 80:8000 \
  tu-usuario/styleyoung:latest
```

---

## 🌐 PARTE 7: Configurar Dominio .tk (Opcional)

### 7.1 Registrar Dominio

1. Ve a [dot.tk](http://www.dot.tk/)
2. Busca `tu-dominio.tk`
3. Selecciona "Free" y completa

### 7.2 Configurar DNS

En dot.tk Management → Manage DNS:

```
Type: A
Name: @
Value: 52.73.136.81
TTL: 3600
```

### 7.3 Actualizar .env en EC2

```bash
nano .env

# Cambiar:
ALLOWED_HOSTS=52.73.136.81,tu-dominio.tk,www.tu-dominio.tk

# Guardar y reiniciar:
docker restart styleyoung_app
```

---

## 🐛 Troubleshooting

### GitHub Actions no construye la imagen

**Solución:**
- Verifica que creaste los secretos `DOCKER_USERNAME` y `DOCKER_PASSWORD`
- Ve a GitHub → Actions y revisa los logs del workflow

### Imagen no se descarga en EC2

**Solución:**
```bash
# Asegúrate que el nombre es correcto:
docker pull tu-usuario/styleyoung:latest

# Verifica en Docker Hub que existe:
# https://hub.docker.com/r/tu-usuario/styleyoung
```

### Puerto 80 ocupado

**Solución:**
```bash
docker run -d \
  --name styleyoung_app \
  --env-file .env \
  -p 8080:8000 \
  tu-usuario/styleyoung:latest

# Acceder en: http://52.73.136.81:8080
```

### Credenciales AWS inválidas

**Solución:**
```bash
nano .env
# Verificar que todo está correcto

docker restart styleyoung_app
docker logs -f styleyoung_app
```

---

## 📊 Comandos Útiles en EC2

```bash
docker ps                                    # Ver contenedores
docker logs -f styleyoung_app               # Ver logs en tiempo real
docker logs --tail=50 styleyoung_app        # Últimas 50 líneas
docker exec styleyoung_app bash             # Entrar en contenedor
docker stop styleyoung_app                  # Detener
docker start styleyoung_app                 # Iniciar
docker restart styleyoung_app               # Reiniciar
docker rm styleyoung_app                    # Eliminar contenedor
docker stats                                # Ver uso de recursos
```

---

## 📝 Resumen Rápido

| Paso | Acción |
|------|--------|
| 1 | Crear cuenta Docker Hub |
| 2 | Crear token en Docker Hub |
| 3 | Crear secretos en GitHub (DOCKER_USERNAME, DOCKER_PASSWORD) |
| 4 | Hacer commit y push a GitHub |
| 5 | GitHub Actions construye y sube imagen automáticamente |
| 6 | SSH a EC2 |
| 7 | Crear `.env` en EC2 |
| 8 | `docker pull tu-usuario/styleyoung:latest` |
| 9 | `docker run -d --name styleyoung_app --env-file .env -p 80:8000 tu-usuario/styleyoung:latest` |
| 10 | Acceder en `http://52.73.136.81` |

---

## 🎯 El Flujo Completo en 10 Minutos

**Vez 1 (Setup inicial):**
1. Crear cuenta Docker Hub
2. Crear token
3. Crear secretos en GitHub
4. Instalar Docker en EC2
5. Crear .env en EC2

**Veces Siguientes (Después de cambios):**
1. `git add .`
2. `git commit -m "cambios"`
3. `git push origin main`
4. Esperar GitHub Actions
5. En EC2: `docker pull` + `docker run`

**¡Y ya está deployado!** 🚀

---

**¡Con esto tienes despliegue completamente automatizado sin Docker en tu PC!** ✨
