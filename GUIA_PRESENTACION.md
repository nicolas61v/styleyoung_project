# 📋 GUÍA RÁPIDA PARA PRESENTACIÓN - StyleYoung

## 🎯 ESTRUCTURA DE LA PRESENTACIÓN (5-10 minutos)

---

## 1️⃣ ARQUITECTURA MVC

**Mostrar en la app:**
- **Modelos:** `tienda/models.py` → Mostrar las 8 entidades (Categoria, Producto, Talla, Pedido, etc.)
- **Vistas:** `tienda/views.py` → 30+ funciones separadas por usuario/admin/API
- **Templates:** `templates/` → carpetas por rol (usuario/, admin/, auth/)

**Ruta para verificar:**
```
http://98.93.219.36/en//es/  → Home (vista + template)
http://98.93.219.36/en//productos/  → Productos (vista + template)
http://98.93.219.36/en//admin-panel/  → Admin (vista + template)
```

---

## 2️⃣ SERVICIOS (Services Layer)

**Ubicación:** `tienda/services/`

**Mostrar carpeta con 4 archivos:**

1. **clima_service.py**
   - Lee: OpenWeatherMap API integration
   - Mostrar en app: Navbar superior derecha con temperatura

2. **reporte_interface.py**
   - Define interfaz abstracta para reportes

3. **reporte_pdf.py**
   - Implementación concreta (PDF)

4. **reporte_excel.py**
   - Implementación concreta (Excel)

**Probar en la app:**
```
http://98.93.219.36/en/admin-panel/reportes/  → Ver reportes
Botones: "Descargar PDF" y "Descargar Excel"
```

---

## 3️⃣ DEPENDENCY INJECTION (DI)

**Mostrar en código:**

```python
# tienda/services/reporte_interface.py
class ReporteInterface(ABC):
    @abstractmethod
    def generar_reporte(self, titulo, datos, columnas) -> HttpResponse:
        pass
```

**Dos implementaciones:**
- `ReportePDF` en `reporte_pdf.py`
- `ReporteExcel` en `reporte_excel.py`

**Beneficio:** Cambiar formato sin modificar vistas

---

## 4️⃣ MULTI-IDIOMA (i18n)

**Mostrar en la app:**
- Click en **idioma selector** (navbar arriba derecha)
- Cambiar entre **Español** y **English**
- Todo el sitio cambio de idioma

**Archivos:**
- `settings.py` → LANGUAGES = [('es', 'Español'), ('en', 'English')]
- `locale/en/LC_MESSAGES/django.po` → 80+ traducciones

---

## 5️⃣ TESTS UNITARIOS

**Correr en terminal:**
```bash
python manage.py test tienda.tests.ProductoTestCase
```

**Resultado:**
```
Ran 2 tests in 0.004s
OK ✓
```

**Qué prueban:**
1. Creación de producto con datos correctos
2. Cálculo de stock total (10+15+8=33)

---

## 6️⃣ API REST

**Acceder a documentación interactiva:**
```
http://3.94.191.93/api/v1/
```

**Probar endpoints en navegador:**
```
http://98.93.219.36/api/v1/productos/
http://98.93.219.36/api/v1/productos/en-stock/
http://98.93.219.36/api/v1/productos/mas-vendidos/
http://98.93.219.36/api/v1/productos/estadisticas/
http://98.93.219.36/api/status/
```

**Características:**
- Paginación (20 por página)
- Filtrado (categoría, marca, color, precio)
- Búsqueda full-text
- Respuestas JSON

---

## 7️⃣ API EXTERNA (Third-party)

**Mostrar en app:**
- Navbar arriba → Widget del clima
- Muestra: Temperatura, descripción, icono
- Consume: **OpenWeatherMap API**

**Código:** `tienda/services/clima_service.py`
- Caching 2 horas
- Retry logic
- Fallback si falla

---

## 8️⃣ DOCKER

**Mostrar archivos:**
- `Dockerfile` → Imagen de la app
- `docker-compose.yml` → 3 servicios (Web, DB, Nginx)
- `.dockerignore` → Qué no incluir

**La app está corriendo en Docker en EC2** ✅

---

## 9️⃣ UI/USABILIDAD

**Mostrar en la app:**

1. **Consistencia Visual**
   - Bootstrap 5
   - Colores: Azul primario, naranja warning
   - Mismas tipografías en toda la app

2. **Navegación**
   - Navbar en todas las páginas
   - Breadcrumbs (Home > Productos > Nombre)
   - Footer en todas las páginas
   - Menú lateral admin

3. **Formularios**
   - No se vacían si hay errores
   - Validación clara
   - Campos bien diseñados (select, textarea, etc.)

4. **Responsivo**
   - Probar en móvil/tablet (F12)
   - Funciona en todos los tamaños

5. **Búsqueda AJAX**
   - Navbar: escribir en buscar
   - Resultados en tiempo real
   - Sin recargar página

---

## 🔟 ADMIN PANEL

**Rutas para mostrar:**

```
http://3.94.191.93/es/admin-panel/  → Dashboard
http://3.94.191.93/es/admin-panel/productos/  → Gestión productos
http://3.94.191.93/es/admin-panel/categorias/  → Gestión categorías
http://3.94.191.93/es/admin-panel/pedidos/  → Gestión pedidos
http://3.94.191.93/es/admin-panel/reportes/  → Reportes
```

**Features:**
- Crear/editar/eliminar productos
- Cambiar estado de pedidos (Pendiente → Procesando → Enviado → Entregado)
- Ver estadísticas en tiempo real
- Descargar reportes PDF/Excel

---

## 1️⃣1️⃣ REPORTES (PDF + Excel)

**Mostrar en app:**
```
http://3.94.191.93/es/admin-panel/reportes/
```

**Botones:**
- "Descargar PDF" → Abre descarga de PDF
- "Descargar Excel" → Abre descarga de Excel

**Datos incluidos:**
- Productos
- Ventas por categoría
- Stock y vendidos
- Tabla de inventario

**Implementación:**
- `ReportePDF` → ReportLab library
- `ReporteExcel` → openpyxl library
- Patrón DI usado

---

## 1️⃣2️⃣ GIT COMMITS

**Ver historial:**
```bash
git log --oneline | head -20
```

**Total: 73 commits**

Ejemplo recientes:
- `baf570b` - DOCS: Agregar documentación de API REST
- `3e0bc33` - FIX: Cambiar logo de imagen a icono
- `2bf56cb` - FEATURE: Agregar banner profesional
- `6acfed6` - FIX: Calcular porcentajes en vista
- Etc...

---

## 📊 FLUJO COMPLETO (Demo)

**Mostrar funcionalidad end-to-end:**

1. **Usuario navega**
   - Home → Ver productos
   - Click en un producto → Ver detalles
   - Agregar al carrito

2. **Checkout**
   - Ir a carrito
   - Click "Confirmar Compra"
   - Llenar dirección
   - Ver confirmación con orden número

3. **Admin verifica**
   - Ir a `/admin-panel/pedidos/`
   - Ver pedido recién creado
   - Cambiar estado (Pendiente → Enviado)
   - Guardar cambio

4. **Reportes**
   - Ir a `/admin-panel/reportes/`
   - Descargar PDF/Excel
   - Mostrar que tiene datos reales

---

## 🎨 EXTRAS DESTACABLES

1. **Banner profesional con carrusel**
   - Home page con imágenes rotando automáticamente
   - Bootstrap carousel component

2. **Búsqueda AJAX**
   - Sin recargar página
   - Resultados instantáneos

3. **Widget de clima**
   - Integración con API externa
   - Muestra temperatura actual

4. **Sistema de tallas**
   - Cada producto tiene tallas
   - Control de stock por talla

5. **Filtros avanzados**
   - Categoría, precio, color, marca, talla, stock

---

## ⏱️ TIMING SUGERIDO

- Arquitectura MVC: 1 min
- Servicios + DI: 1 min
- Multi-idioma: 30 seg
- Tests: 30 seg
- API REST: 1 min
- API Externa: 30 seg
- Docker: 30 seg
- UI/Usabilidad: 1 min
- Admin Panel: 1 min
- Reportes: 1 min
- Demo flujo completo: 2-3 min

**Total: 10-12 minutos** ✅

---

## 📌 PUNTOS CLAVE A RESALTAR

✅ Todo lo del Entregable 2 está implementado
✅ 73 commits mostrando desarrollo iterativo
✅ Arquitectura profesional y escalable
✅ Código limpio y bien estructurado
✅ Totalmente desplegado en AWS EC2
✅ Tests pasando correctamente
✅ API lista para consumo externo
✅ Experiencia de usuario optimizada

---

**¡Listo para presentación! 🚀**
