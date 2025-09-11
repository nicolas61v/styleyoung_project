# StyleYoung - Funcionalidades Implementadas

## ============================================
## WIKI - PÁGINA: "Funcionalidades Interesantes" 
## ============================================

### 1. **Búsqueda AJAX en Tiempo Real**
- **Descripción**: Búsqueda instantánea de productos mientras el usuario escribe
- **Ubicación**: `tienda/views.py:136-169`
- **Funcionalidad**: Busca en nombre, marca, descripción, categoría, color y material
- **Límite**: 10 resultados máximo
- **Respuesta**: JSON con datos del producto

### 2. **Top 3 Productos Más Vendidos (Dinámico)**
- **Descripción**: Muestra los productos más vendidos basado en datos reales
- **Ubicación Modelo**: `tienda/models.py:67-70` (método `get_top_vendidos`)
- **Ubicación Vista**: `tienda/views.py:194` (dashboard admin)
- **Funcionalidad**: Actualización automática basada en pedidos entregados

### 3. **Sistema de Filtros Avanzados**
- **Descripción**: Filtros combinables por múltiples criterios
- **Ubicación**: `tienda/views.py:29-97`
- **Filtros disponibles**:
  - Por categoría
  - Rango de precios (min/max)
  - Color
  - Marca
  - Talla (con stock disponible)
  - Solo productos en stock
  - Búsqueda de texto

### 4. **Dashboard Ejecutivo con Métricas**
- **Descripción**: Panel de control con estadísticas en tiempo real
- **Ubicación**: `tienda/views.py:176-221`
- **Métricas incluidas**:
  - Total productos, pedidos, categorías
  - Productos con stock bajo (<5 unidades)
  - Ventas del mes actual
  - Pedidos completados del mes
  - Pedidos recientes (últimos 5)

### 5. **Actualización Automática de Contadores de Ventas**
- **Descripción**: Sistema que actualiza automáticamente productos vendidos
- **Ubicación**: `tienda/models.py:55-79` (métodos `actualizar_ventas` y `actualizar_todas_las_ventas`)
- **Ubicación Vista**: `tienda/views.py:282-292`
- **Funcionalidad**: Cuenta pedidos entregados para estadísticas precisas

### 6. **Reportes y Análisis por Categoría**
- **Descripción**: Análisis de ventas segmentado por categoría
- **Ubicación**: `tienda/views.py:254-278`
- **Funcionalidad**: Ventas totales por categoría ordenadas descendentemente

## ============================================
## WIKI - PÁGINA: "Guía de Estilo de Programación"
## ============================================

### **Convenciones de Código**
- **Idioma**: Español para nombres de variables y comentarios
- **Naming**: snake_case para funciones y variables, PascalCase para clases
- **Documentación**: Docstrings en español para métodos principales
- **Imports**: Organizados por grupos (Django, terceros, locales)

### **Estructura de Archivos**
- **Models**: Lógica de negocio en métodos de modelo
- **Views**: Separación clara usuario final vs administrador
- **Templates**: Herencia de base.html, organización por módulos
- **URLs**: Estructura jerárquica con nombres descriptivos

### **Estándares Django**
- **Decorators**: Uso de @login_required y @user_passes_test
- **QuerySets**: Optimización con select_related y prefetch_related
- **Forms**: Validaciones personalizadas cuando sea necesario
- **Static Files**: Organización en carpetas por módulo

## ============================================
## WIKI - PÁGINA: "Reglas de Programación"
## ============================================

### **Reglas para Modelos**
- Todo modelo debe tener método `__str__()` descriptivo
- Usar Meta class para verbose_name en español
- Métodos de negocio deben estar en el modelo, no en views
- Relaciones con on_delete explícito

### **Reglas para Views**
- Separar vistas de usuario final y administrador
- Usar decorators para control de acceso
- Validar permisos antes de operaciones críticas
- Funciones de utilidad como `es_admin()`

### **Reglas para Templates**
- Todos los templates deben extender de base.html
- Usar nombres descriptivos para blocks
- Organizar en carpetas por módulo (usuario/, admin/)
- Templates HTML válidos

### **Reglas para URLs**
- Todas las rutas deben tener nombre único
- Usar namespaces para evitar conflictos
- URLs descriptivas y RESTful
- Documentar propósito en comentarios

## ============================================
## INFORMACIÓN ADICIONAL PARA DOCUMENTACIÓN
## ============================================

### **Modelos Implementados**
- **Usuario**: Modelo personalizado extendido de AbstractUser
- **Categoria**: Gestión de categorías de productos
- **Producto**: Entidad principal con métodos de negocio
- **Talla**: Gestión granular de stock por talla
- **CarritoCompras**: Sistema de carrito persistente
- **ItemCarrito**: Items individuales del carrito
- **Pedido**: Gestión de órdenes con estados
- **ItemPedido**: Detalle de productos por pedido

### **Sistema de Autenticación**
- **Modelo personalizado**: Email como username
- **Separación de roles**: Usuario final vs Administrador
- **Login diferenciado**: Rutas separadas para cada tipo de usuario

### **Estructura MVT Django**
- **Models**: `tienda/models.py`, `usuarios/models.py`
- **Views**: `tienda/views.py`, `usuarios/views.py`
- **Templates**: Organizados en `templates/usuario/` y `templates/admin/`
- **URLs**: Rutas organizadas jerárquicamente

### **Características Técnicas**

**Base de Datos**
- **SQLite3**: Para desarrollo
- **Migrations**: Sistema completo de migraciones implementado
- **Relaciones**: Foreign Keys y relaciones Many-to-Many bien definidas

**Frontend**
- **AJAX**: Búsqueda en tiempo real sin recarga de página
- **Responsive**: Diseño adaptable
- **Templates heredados**: Sistema de herencia con `base.html`

**Backend**
- **Django 5.0.6**: Framework principal
- **Decorators**: `@login_required`, `@user_passes_test`
- **QuerySets optimizados**: Consultas eficientes con `select_related`
- **Validaciones**: Métodos de validación en modelos

### **Gestión de Stock y Pedidos**

**Control de Inventario**
- **Stock por talla**: Gestión granular
- **Verificación automática**: Antes de procesar pedidos
- **Alertas**: Productos con stock bajo en dashboard
- **Reducción automática**: Al procesar pedidos

**Flujo de Pedidos**
1. **Carrito**: Agregado de productos con talla específica
2. **Pedido**: Conversión de carrito a pedido
3. **Estados**: Pendiente → Procesando → Enviado → Entregado
4. **Stock**: Reducción automática al procesar

### **Funciones de Utilidad**

**Métodos de Negocio en Modelos**
- `Producto.obtener_detalles()`: Información completa del producto
- `Producto.stock_total()`: Suma stock de todas las tallas
- `CarritoCompras.calcular_total()`: Cálculo automático de totales
- `Talla.verificar_stock()`: Validación de disponibilidad

**APIs AJAX**
- `/api/busqueda/`: Búsqueda en tiempo real
- `/api/actualizar-ventas/`: Actualización manual de contadores
- `/api/status/`: Estado de la aplicación

### **Reportes y Estadísticas**

**Dashboard Administrativo**
- Métricas de rendimiento en tiempo real
- Top productos más vendidos
- Análisis temporal (mes actual)
- Gestión de stock crítico

**Sistema de Reportes**
- Ventas por categoría
- Productos más vendidos
- Análisis de inventario
- Seguimiento de pedidos