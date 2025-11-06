# 📡 API REST de StyleYoung - Documentación Completa

## 🌟 Descripción

API REST pública para consumo de productos de StyleYoung - Tienda Virtual de Ropa.

**Base URL:** `http://tu-dominio.com/api/v1/`

**Versión:** 1.0

---

## 🚀 Características

- ✅ **API Pública** - Sin autenticación requerida
- ✅ **CORS Habilitado** - Puede ser consumida desde cualquier origen
- ✅ **Paginación Automática** - 20 items por página
- ✅ **Filtros Avanzados** - Por categoría, marca, color, precio
- ✅ **Búsqueda Flexible** - Por nombre, marca, descripción, material
- ✅ **Imágenes en S3** - URLs completas de imágenes
- ✅ **Formato JSON** - Respuestas estructuradas

---

## 📋 Endpoints Disponibles

### 1. **Información de la API**

```http
GET /api/v1/
```

Retorna información general de la API y todos los endpoints disponibles.

**Respuesta:**
```json
{
  "mensaje": "Bienvenido a la API de StyleYoung",
  "version": "1.0",
  "endpoints": {...},
  "parametros_busqueda": {...},
  "ejemplos": {...}
}
```

---

### 2. **Lista de Productos**

```http
GET /api/v1/productos/
```

Retorna todos los productos con paginación.

**Parámetros de búsqueda:**
- `search` - Buscar en nombre, marca, descripción
- `categoria` - Filtrar por ID de categoría
- `marca` - Filtrar por marca
- `color` - Filtrar por color
- `precio_min` - Precio mínimo
- `precio_max` - Precio máximo
- `ordering` - Ordenar por precio, -precio, fecha_creacion, etc.
- `page` - Número de página

**Ejemplos:**
```http
GET /api/v1/productos/
GET /api/v1/productos/?search=camiseta
GET /api/v1/productos/?marca=Nike
GET /api/v1/productos/?categoria=1
GET /api/v1/productos/?precio_max=50000
GET /api/v1/productos/?ordering=-total_vendidos
GET /api/v1/productos/?page=2
```

**Respuesta:**
```json
{
  "count": 50,
  "next": "http://api.com/api/v1/productos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "Camiseta Básica",
      "precio": 45000.00,
      "marca": "Nike",
      "color": "Blanco",
      "categoria_nombre": "Ropa Casual",
      "imagen_url": "https://s3.amazonaws.com/...",
      "stock_total": 25,
      "total_vendidos": 10
    }
  ]
}
```

---

### 3. **Detalle de Producto**

```http
GET /api/v1/productos/{id}/
```

Retorna información completa de un producto específico.

**Ejemplo:**
```http
GET /api/v1/productos/1/
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Camiseta Básica",
  "descripcion": "Camiseta de algodón 100%",
  "precio": 45000.00,
  "marca": "Nike",
  "color": "Blanco",
  "material": "Algodón",
  "categoria": {
    "id": 1,
    "nombre": "Ropa Casual",
    "descripcion": "...",
    "total_productos": 15
  },
  "imagen_principal_url": "https://s3.amazonaws.com/...",
  "imagenes": [
    {
      "id": 1,
      "imagen_url": "https://s3.amazonaws.com/...",
      "descripcion": "Vista frontal",
      "es_principal": true,
      "orden": 1
    }
  ],
  "tallas": [
    {
      "id": 1,
      "talla": "S",
      "stock": 10
    },
    {
      "id": 2,
      "talla": "M",
      "stock": 15
    }
  ],
  "stock_total": 25,
  "total_vendidos": 10,
  "fecha_creacion": "2024-01-15T10:30:00Z",
  "url_detalle": "http://tu-dominio.com/producto/1/",
  "disponible": true
}
```

---

### 4. **Productos en Stock**

```http
GET /api/v1/productos/en-stock/
```

Retorna solo productos que tienen stock disponible.

**Respuesta:** Mismo formato que lista de productos, pero filtrados por stock > 0

---

### 5. **Productos Más Vendidos**

```http
GET /api/v1/productos/mas-vendidos/
```

Retorna los 10 productos más vendidos.

---

### 6. **Estadísticas de Productos**

```http
GET /api/v1/productos/estadisticas/
```

Retorna estadísticas generales.

**Respuesta:**
```json
{
  "total_productos": 50,
  "productos_disponibles": 45,
  "productos_agotados": 5,
  "total_ventas": 500,
  "categorias_activas": 8
}
```

---

### 7. **Lista de Categorías**

```http
GET /api/v1/categorias/
```

Retorna todas las categorías.

**Respuesta:**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "nombre": "Ropa Casual",
      "descripcion": "...",
      "total_productos": 15
    }
  ]
}
```

---

### 8. **Detalle de Categoría**

```http
GET /api/v1/categorias/{id}/
```

---

### 9. **Productos de una Categoría**

```http
GET /api/v1/categorias/{id}/productos/
```

Retorna todos los productos de una categoría específica.

---

## 💻 Ejemplos de Consumo

### JavaScript (Fetch API)

```javascript
// Obtener lista de productos
fetch('http://tu-dominio.com/api/v1/productos/')
  .then(response => response.json())
  .then(data => {
    console.log(`Total productos: ${data.count}`);
    data.results.forEach(producto => {
      console.log(`${producto.nombre} - $${producto.precio}`);
    });
  });

// Buscar productos
fetch('http://tu-dominio.com/api/v1/productos/?search=camiseta&precio_max=50000')
  .then(response => response.json())
  .then(data => console.log(data));

// Obtener detalle de producto
fetch('http://tu-dominio.com/api/v1/productos/1/')
  .then(response => response.json())
  .then(producto => {
    console.log(producto.nombre);
    console.log('Tallas disponibles:', producto.tallas);
  });
```

---

### Python (requests)

```python
import requests

# Obtener productos
response = requests.get('http://tu-dominio.com/api/v1/productos/')
data = response.json()

for producto in data['results']:
    print(f"{producto['nombre']} - ${producto['precio']}")

# Buscar productos por marca
response = requests.get('http://tu-dominio.com/api/v1/productos/', params={
    'marca': 'Nike',
    'ordering': '-precio'
})
productos = response.json()
```

---

### cURL

```bash
# Lista de productos
curl http://tu-dominio.com/api/v1/productos/

# Buscar camisetas
curl "http://tu-dominio.com/api/v1/productos/?search=camiseta"

# Detalle de producto
curl http://tu-dominio.com/api/v1/productos/1/

# Productos en stock
curl http://tu-dominio.com/api/v1/productos/en-stock/

# Estadísticas
curl http://tu-dominio.com/api/v1/productos/estadisticas/
```

---

## 🔧 Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 📝 Notas Importantes

1. **Sin Autenticación:** Esta API es pública y no requiere autenticación
2. **CORS:** Habilitado para todos los orígenes
3. **Paginación:** Por defecto 20 items por página
4. **Imágenes:** Las URLs son absolutas e incluyen el dominio completo
5. **Formato:** Todas las respuestas son JSON
6. **S3:** Las imágenes se sirven desde AWS S3 (cuando está configurado)

---

## 🚀 Para Otros Equipos

Esta API puede ser consumida por cualquier aplicación que necesite mostrar productos de StyleYoung:

1. **Frontend en React/Vue/Angular**
2. **Aplicaciones Móviles (iOS/Android)**
3. **Otras aplicaciones Django**
4. **Sitios WordPress**
5. **Cualquier cliente HTTP**

**No se requiere permiso especial** - la API es completamente pública.

---

## 📧 Soporte

Para preguntas o problemas con la API, contactar al equipo de StyleYoung.

**Proyecto:** StyleYoung - Tienda Virtual de Ropa
**Versión API:** 1.0
**Última actualización:** 2024
