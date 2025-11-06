# 🚀 GUÍA COMPLETA: Configurar AWS S3 para StyleYoung

## 📋 Índice
1. [Crear Bucket en S3](#1-crear-bucket-en-s3)
2. [Configurar Permisos](#2-configurar-permisos)
3. [Obtener Credenciales](#3-obtener-credenciales-aws)
4. [Configurar Django](#4-configurar-django)
5. [Subir Imágenes a S3](#5-subir-imágenes-a-s3)
6. [Consumir la API](#6-consumir-tu-propia-api)

---

## 1. 🪣 CREAR BUCKET EN S3

### Paso 1: Acceder a AWS Console
1. Ve a https://aws.amazon.com/console/
2. Inicia sesión con tu cuenta AWS
3. Busca "S3" en la barra de búsqueda
4. Click en "S3" para abrir el servicio

### Paso 2: Crear nuevo Bucket
1. Click en "Create bucket" (Crear bucket)
2. **Nombre del bucket:** `styleyoung-productos` (debe ser único globalmente)
3. **Región:** Elige `US East (N. Virginia)` o la más cercana
4. **Object Ownership:** ACLs enabled
5. **Block Public Access:** **DESMARCAR** "Block all public access"
   - ⚠️ Confirmar que quieres hacer el bucket público
6. **Bucket Versioning:** Disabled (opcional)
7. **Default encryption:** Enable (Amazon S3-managed keys)
8. Click en **"Create bucket"**

✅ Bucket creado correctamente

---

## 2. 🔓 CONFIGURAR PERMISOS

### Paso 1: Configurar Bucket Policy

1. Click en el bucket que acabas de crear
2. Ve a la pestaña **"Permissions"** (Permisos)
3. Scroll hasta **"Bucket policy"**
4. Click en **"Edit"**
5. Pega esta política (reemplaza `styleyoung-productos` con tu nombre de bucket):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::styleyoung-productos/*"
        }
    ]
}
```

6. Click en **"Save changes"**

### Paso 2: Configurar CORS

1. En la misma pestaña "Permissions"
2. Scroll hasta **"Cross-origin resource sharing (CORS)"**
3. Click en **"Edit"**
4. Pega esta configuración:

```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

5. Click en **"Save changes"**

✅ Permisos configurados correctamente

---

## 3. 🔑 OBTENER CREDENCIALES AWS

### Opción A: Crear Usuario IAM (Recomendado)

1. Ve al servicio **IAM** (Identity and Access Management)
2. Click en **"Users"** → **"Create user"**
3. **User name:** `styleyoung-s3-user`
4. Click **"Next"**
5. **Permissions:**
   - Select **"Attach policies directly"**
   - Busca y selecciona **"AmazonS3FullAccess"**
6. Click **"Next"** → **"Create user"**

### Crear Access Key

1. Click en el usuario que acabas de crear
2. Ve a la pestaña **"Security credentials"**
3. Scroll hasta **"Access keys"**
4. Click en **"Create access key"**
5. Select **"Application running on an AWS compute service"**
6. Click **"Next"** → **"Create access key"**

7. **¡IMPORTANTE! Guarda estos datos:**
   ```
   Access Key ID: AKIAIOSFODNN7EXAMPLE
   Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   ```

⚠️ **NUNCA compartas estas credenciales públicamente**

✅ Credenciales obtenidas

---

## 4. ⚙️ CONFIGURAR DJANGO

### Paso 1: Actualizar settings.py

Edita `/styleyoung_project/settings.py`:

```python
# Al inicio del archivo
import os

# Cambiar USE_S3 a True
USE_S3 = True  # ← Cambiar de False a True

if USE_S3:
    # Credenciales AWS (USAR VARIABLES DE ENTORNO EN PRODUCCIÓN)
    AWS_ACCESS_KEY_ID = 'TU_ACCESS_KEY_ID'  # ← Pegar tu Access Key
    AWS_SECRET_ACCESS_KEY = 'TU_SECRET_ACCESS_KEY'  # ← Pegar tu Secret Key
    AWS_STORAGE_BUCKET_NAME = 'styleyoung-productos'  # ← Tu bucket name
    AWS_S3_REGION_NAME = 'us-east-1'  # ← Tu región

    # S3 Configuration
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_LOCATION = 'media'

    # Media files (uploads) en S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
```

### Paso 2: Variables de Entorno (Producción)

Para producción, crea un archivo `.env`:

```bash
# .env (NO subir a GitHub)
AWS_ACCESS_KEY_ID=tu_access_key_aqui
AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
AWS_STORAGE_BUCKET_NAME=styleyoung-productos
AWS_S3_REGION_NAME=us-east-1
USE_S3=True
```

Y en `settings.py`:

```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de .env

USE_S3 = os.getenv('USE_S3', 'False') == 'True'

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    # ... resto de configuración
```

✅ Django configurado para S3

---

## 5. 📤 SUBIR IMÁGENES A S3

### Opción A: A través del Admin de Django

1. Inicia el servidor: `python manage.py runserver`
2. Ve al admin: http://localhost:8000/admin-panel/
3. Crea o edita un producto
4. Sube una imagen
5. **Automáticamente se subirá a S3**

### Opción B: Script para migrar imágenes existentes

Crea `migrate_to_s3.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'styleyoung_project.settings')
django.setup()

from tienda.models import Producto
from django.core.files import File

# Migrar imágenes locales a S3
for producto in Producto.objects.all():
    if producto.imagen_principal:
        # Django automáticamente subirá a S3
        producto.save()
        print(f"✓ {producto.nombre} - imagen migrada a S3")
```

Ejecutar:
```bash
python migrate_to_s3.py
```

### Opción C: Subir directamente con AWS CLI

```bash
# Instalar AWS CLI
pip install awscli

# Configurar credenciales
aws configure

# Subir archivos
aws s3 cp bancoImagenes/ s3://styleyoung-productos/media/ --recursive
```

✅ Imágenes en S3

---

## 6. 🔄 CONSUMIR TU PROPIA API

### ¿Por qué consumir tu propia API?

1. **Demostrar que funciona** para otros equipos
2. **Testear la API** en producción
3. **Cumplir el requisito** del taller

### Ver la API funcionando

1. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

2. Abre en el navegador:
   ```
   http://localhost:8000/api/v1/
   ```

3. Verás la documentación interactiva de la API

4. Prueba los endpoints:
   ```
   http://localhost:8000/api/v1/productos/
   http://localhost:8000/api/v1/productos/en-stock/
   http://localhost:8000/api/v1/productos/1/
   ```

### Ver imágenes desde S3

Las URLs de las imágenes serán:
```
https://styleyoung-productos.s3.amazonaws.com/media/productos/imagen.jpg
```

✅ API funcionando con S3

---

## 7. 🐳 DEPLOYMENT CON DOCKER

### Dockerfile ya configurado

El proyecto ya tiene `Dockerfile` y `docker-compose.yml`

### Desplegar en AWS (EC2 o ECS)

```bash
# 1. Build la imagen
docker build -t styleyoung-api .

# 2. Correr el contenedor
docker run -p 8000:8000 \
  -e USE_S3=True \
  -e AWS_ACCESS_KEY_ID=tu_key \
  -e AWS_SECRET_ACCESS_KEY=tu_secret \
  styleyoung-api
```

### Con docker-compose:

```bash
docker-compose up -d
```

✅ Desplegado con Docker

---

## 📊 RESUMEN DE COSTOS AWS

### S3 (Gratis tier - 12 meses)
- ✅ 5 GB de almacenamiento estándar
- ✅ 20,000 solicitudes GET
- ✅ 2,000 solicitudes PUT

Para un proyecto escolar, **completamente gratis**.

---

## ⚠️ IMPORTANTE: SEGURIDAD

### ✅ HACER:
- Usar variables de entorno para credenciales
- Nunca subir `.env` a GitHub
- Agregar `.env` al `.gitignore`
- Usar políticas IAM específicas
- Rotar credenciales regularmente

### ❌ NO HACER:
- Hardcodear credenciales en `settings.py`
- Subir credenciales a GitHub
- Dar permisos de administrador
- Compartir Access Keys públicamente

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Access Denied"
- Verificar Bucket Policy
- Verificar credenciales AWS
- Verificar región correcta

### Error: "No module named 'storages'"
```bash
pip install django-storages boto3
```

### Imágenes no se ven
- Verificar que USE_S3=True
- Verificar URL del bucket
- Verificar permisos públicos

---

## ✅ CHECKLIST COMPLETO

- [ ] Cuenta AWS creada
- [ ] Bucket S3 creado
- [ ] Bucket Policy configurada
- [ ] CORS configurado
- [ ] Usuario IAM creado
- [ ] Access Keys generadas
- [ ] `settings.py` actualizado con credenciales
- [ ] Variables de entorno configuradas
- [ ] Imágenes subidas a S3
- [ ] API funcionando en `/api/v1/`
- [ ] Endpoints probados
- [ ] Docker configurado
- [ ] `.env` en `.gitignore`

---

## 🎓 PARA LA SUSTENTACIÓN

Puedes demostrar:

1. **API Funcionando:**
   - Mostrar `http://localhost:8000/api/v1/`
   - Mostrar endpoints de productos
   - Mostrar imágenes desde S3

2. **Consumo Propio:**
   - Abrir consola del navegador
   - Hacer fetch a tu propia API
   - Mostrar JSON response

3. **Imágenes en S3:**
   - Mostrar bucket en AWS Console
   - Mostrar URLs completas
   - Demostrar acceso público

---

## 📞 RECURSOS ADICIONALES

- [Documentación Django Storages](https://django-storages.readthedocs.io/)
- [Documentación AWS S3](https://docs.aws.amazon.com/s3/)
- [Documentación DRF](https://www.django-rest-framework.org/)

**¡Éxito en tu proyecto!** 🚀
