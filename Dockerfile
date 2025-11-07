# Dockerfile para StyleYoung - Tienda Virtual de Ropa
# Python 3.12 base image
FROM python:3.12-slim

# Información del maintainer
LABEL maintainer="StyleYoung Team"
LABEL description="Tienda Virtual de Ropa para Jóvenes"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=styleyoung_project.settings

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    gettext \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código del proyecto
COPY . /app/

# Crear directorios para archivos estáticos, media y base de datos
RUN mkdir -p /app/staticfiles /app/media /app/db

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput || true

# Compilar mensajes de traducción (si existen)
RUN python manage.py compilemessages || true

# Exponer puerto 8000
EXPOSE 8000

# Crear usuario no-root para ejecutar la aplicación
RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

# Comando por defecto para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "styleyoung_project.wsgi:application"]
