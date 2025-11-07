# StyleYoung - Tienda Virtual de Ropa

## Descripción del Proyecto

**StyleYoung** es una plataforma de comercio electrónico especializada en la venta de ropa online, desarrollada con Django 5.0.6. El proyecto implementa un sistema completo de e-commerce con funcionalidades diferenciadas para usuarios finales y administradores, ofreciendo una experiencia de compra moderna y eficiente

### Propósito
Crear una solución integral de comercio electrónico que permita a las tiendas de ropa gestionar su inventario, procesar pedidos y ofrecer una experiencia de compra optimizada a sus clientes.

---

## Alcance del Proyecto

### Funcionalidades Implementadas

#### **Usuario Final**
- **Catálogo de Productos**: Navegación y búsqueda con filtros avanzados
- **Sistema de Filtros**: Por categoría, precio, color, marca, talla y stock
- **Búsqueda en Tiempo Real**: AJAX para resultados instantáneos
- **Detalle de Producto**: Información completa con selector de tallas
- **Carrito de Compras**: Gestión completa de productos seleccionados
- **Sistema de Pedidos**: Seguimiento desde creación hasta entrega
- **Autenticación**: Registro y login personalizado

#### **Administrador**
- **Dashboard Ejecutivo**: Métricas y estadísticas en tiempo real
- **Gestión de Inventario**: CRUD completo de productos y categorías
- **Control de Stock**: Alertas de productos con stock bajo
- **Gestión de Pedidos**: Estados y seguimiento completo
- **Reportes Dinámicos**: Top productos más vendidos y análisis por categoría
- **Sistema de Tallas**: Gestión granular por producto

### Tecnologías Utilizadas
- **Backend**: Django 5.0.6, Python
- **Base de Datos**: SQLite (desarrollo)
- **Frontend**: HTML5, CSS3, JavaScript (AJAX)
- **Autenticación**: Sistema personalizado con modelo de usuario extendido
- **Configuración**: Español (Colombia), zona horaria America/Bogota

---

## Actores Involucrados

### 1. **Cliente Final**
- **Rol**: Usuario que realiza compras
- **Responsabilidades**:
  - Navegar el catálogo de productos
  - Realizar búsquedas y aplicar filtros
  - Gestionar su carrito de compras
  - Realizar pedidos y seguimiento
  - Gestionar su perfil y datos personales

### 2. **Administrador de Tienda**
- **Rol**: Personal encargado de la gestión operativa
- **Responsabilidades**:
  - Gestionar inventario (productos, categorías, stock)
  - Procesar y gestionar pedidos
  - Monitorear métricas de ventas
  - Generar reportes de rendimiento
  - Mantener actualizada la información de productos

### 3. **Super Administrador**
- **Rol**: Administrador técnico del sistema
- **Responsabilidades**:
  - Configuración del sistema Django
  - Gestión de usuarios administradores
  - Respaldo y mantenimiento de datos
  - Supervisión técnica de la plataforma

---

## Beneficios de la Propuesta

### **Para el Negocio**
- **Automatización**: Reduce trabajo manual en gestión de inventario
- **Escalabilidad**: Arquitectura preparada para crecimiento
- **Métricas**: Datos en tiempo real para toma de decisiones
- **Eficiencia**: Proceso de venta completamente digitalizado
- **Alcance**: Venta 24/7 sin limitaciones geográficas

### **Para los Clientes**
- **Experiencia Optimizada**: Búsqueda y filtros avanzados
- **Conveniencia**: Compras desde cualquier dispositivo
- **Transparencia**: Seguimiento completo de pedidos
- **Personalización**: Sistema de tallas y preferencias
- **Rapidez**: Búsqueda en tiempo real con AJAX

### **Técnicos**
- **Rendimiento**: Arquitectura Django optimizada
- **Mantenibilidad**: Código modular y bien estructurado
- **Seguridad**: Sistema de autenticación robusto
- **Flexibilidad**: Fácil extensión y personalización
- **Confiabilidad**: Gestión de estados y validaciones completas

---

## Arquitectura del Sistema

### **Módulos Principales**

#### **Tienda** (`tienda/`)
- **Modelos**: Producto, Categoria, CarritoCompras, Pedido, Talla
- **Funcionalidades**: Catálogo, filtros, carrito, procesamiento pedidos
- **APIs**: Búsqueda AJAX, actualización de contadores

#### **Usuarios** (`usuarios/`)
- **Modelo**: Usuario personalizado (AbstractUser)
- **Autenticación**: Email como username, campos adicionales
- **Roles**: Cliente final y administrador diferenciados

### **Base de Datos**
```
Entidades Principales:
├── Usuario (personalizado)
├── Categoria
├── Producto 
│   └── Talla (relación 1:N)
├── CarritoCompras
│   └── ItemCarrito
└── Pedido
    └── ItemPedido
```

---

## Casos de Uso Principales

1. **Compra Completa**: Cliente busca → filtra → selecciona → carrito → pedido
2. **Gestión de Inventario**: Admin añade productos → configura tallas → controla stock
3. **Procesamiento de Pedidos**: Cliente compra → Admin procesa → entrega → seguimiento
4. **Análisis de Ventas**: Admin consulta reportes → identifica tendencias → toma decisiones

---

## Valor Agregado

- **Escalable**: Preparado para múltiples tiendas y productos
- **Moderno**: Búsqueda en tiempo real y experiencia fluida  
- **Completo**: Desde catálogo hasta reportes ejecutivos
- **Profesional**: Separación clara de responsabilidades usuario/admin
- **Extensible**: Arquitectura Django permite fácil crecimiento

---

## API REST

StyleYoung proporciona una API REST completa para la integración con otras aplicaciones.

### **Endpoints Disponibles**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/productos/` | GET | Lista completa de productos con paginación |
| `/api/v1/productos/{id}/` | GET | Detalle de un producto específico |
| `/api/v1/productos/en-stock/` | GET | Solo productos con stock disponible |
| `/api/v1/productos/mas-vendidos/` | GET | Top 10 productos más vendidos |
| `/api/v1/productos/estadisticas/` | GET | Estadísticas agregadas de la tienda |
| `/api/v1/categorias/` | GET | Lista de categorías disponibles |
| `/api/productos-en-stock/` | GET | Servicio JSON personalizado de productos |
| `/api/status/` | GET | Verificar estado de la API |

### **Características**
- Respuestas en formato JSON
- Paginación: 20 productos por página
- Filtrado por categoría, marca, color y precio
- Búsqueda full-text
- Documentación interactiva en `/api/v1/`

### **Ejemplo de Consumo**
```bash
curl http://3.94.191.93/api/v1/productos/
curl http://3.94.191.93/api/v1/productos/en-stock/
curl http://3.94.191.93/api/status/
```

---

## Despliegue

El proyecto StyleYoung fue desplegado en la nube de Amazon Web Services (AWS), demostrando su funcionamiento en un entorno real. La aplicación cuenta con una API REST que permite mostrar sus productos y ofrece integración con otras aplicaciones.

**Infraestructura:**
- Hosting: AWS EC2
- Almacenamiento de archivos estáticos y multimedia: Amazon S3
- Containerización: Docker

Este despliegue permite una mayor escalabilidad, disponibilidad y gestión centralizada de recursos, garantizando el correcto funcionamiento del sistema en producción.

*StyleYoung representa una solución integral para el comercio electrónico de moda, combinando funcionalidad robusta con experiencia de usuario optimizada.*

