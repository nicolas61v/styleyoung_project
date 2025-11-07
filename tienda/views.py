from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.views.generic import ListView
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Producto, Categoria, CarritoCompras, Pedido, Talla, ImagenProducto
from .forms import ProductoForm, CategoriaForm, ImagenProductoForm, TallaFormSet
from .services.reporte_interface import ReporteInterface
from .services.reporte_pdf import ReportePDF
from .services.reporte_excel import ReporteExcel


def es_admin(user):
    """Verificar si el usuario es administrador"""
    return user.is_staff


# ======================
# VISTAS USUARIO FINAL
# ======================

def home(request):
    """Homepage para usuarios finales"""
    productos_destacados = Producto.objects.all()[:6]
    categorias = Categoria.objects.all()
    return render(request, 'usuario/home.html', {
        'productos_destacados': productos_destacados,
        'categorias': categorias
    })


def productos_lista(request):
    """Catálogo de productos para usuarios finales con filtros avanzados"""
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    # Obtener valores únicos para filtros
    colores_disponibles = Producto.objects.values_list('color', flat=True).distinct().order_by('color')
    marcas_disponibles = Producto.objects.values_list('marca', flat=True).distinct().order_by('marca')
    tallas_disponibles = Talla.objects.values_list('talla', flat=True).distinct().order_by('talla')
    
    # Aplicar filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    # Filtro por rango de precio
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    # Filtro por color
    color = request.GET.get('color')
    if color:
        productos = productos.filter(color__iexact=color)
    
    # Filtro por marca
    marca = request.GET.get('marca')
    if marca:
        productos = productos.filter(marca__iexact=marca)
    
    # Filtro por talla (productos que tienen esa talla disponible)
    talla = request.GET.get('talla')
    if talla:
        productos = productos.filter(talla__talla=talla, talla__stock__gt=0).distinct()
    
    # Filtro solo productos en stock
    solo_stock = request.GET.get('solo_stock')
    if solo_stock:
        productos_con_stock = []
        for producto in productos:
            if producto.stock_total() > 0:
                productos_con_stock.append(producto.id)
        productos = productos.filter(id__in=productos_con_stock)
    
    # Búsqueda de texto
    busqueda = request.GET.get('busqueda')
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(marca__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(categoria__nombre__icontains=busqueda) |
            Q(color__icontains=busqueda) |
            Q(material__icontains=busqueda)
        ).distinct()
    
    # Ordenar por fecha de creación
    productos = productos.order_by('-fecha_creacion')

    # Paginación
    paginator = Paginator(productos, 9)  # 9 productos por página (3x3 grid)
    page = request.GET.get('page')

    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, mostrar la primera página
        productos_paginados = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, mostrar la última página
        productos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'usuario/productos.html', {
        'productos': productos_paginados,
        'categorias': categorias,
        'colores_disponibles': colores_disponibles,
        'marcas_disponibles': marcas_disponibles,
        'tallas_disponibles': tallas_disponibles,
    })


def producto_detalle(request, producto_id):
    """Detalle de producto para usuarios finales"""
    producto = get_object_or_404(Producto, id=producto_id)
    tallas_disponibles = producto.talla_set.filter(stock__gt=0)
    
    return render(request, 'usuario/producto_detalle.html', {
        'producto': producto,
        'tallas_disponibles': tallas_disponibles
    })


@login_required
def carrito(request):
    """Carrito de compras del usuario"""
    carrito, created = CarritoCompras.objects.get_or_create(
        usuario=request.user,
        activo=True
    )
    items = carrito.itemcarrito_set.all()

    return render(request, 'usuario/carrito.html', {
        'carrito': carrito,
        'items': items
    })


@login_required
def agregar_al_carrito(request, producto_id):
    """Agregar producto al carrito"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        talla_id = request.POST.get('talla_id')
        cantidad = int(request.POST.get('cantidad', 1))

        if not talla_id:
            messages.error(request, 'Debes seleccionar una talla.')
            return redirect('tienda:producto_detalle', producto_id=producto_id)

        talla = get_object_or_404(Talla, id=talla_id, producto=producto)

        # Verificar stock disponible
        if talla.stock < cantidad:
            messages.error(request, f'Solo hay {talla.stock} unidades disponibles de la talla {talla.talla}.')
            return redirect('tienda:producto_detalle', producto_id=producto_id)

        # Obtener o crear carrito
        carrito, created = CarritoCompras.objects.get_or_create(
            usuario=request.user,
            activo=True
        )

        # Agregar producto al carrito
        carrito.agregar_producto(producto, talla, cantidad)

        messages.success(request, f'¡{producto.nombre} agregado al carrito!')
        return redirect('tienda:carrito')

    return redirect('tienda:producto_detalle', producto_id=producto_id)


@login_required
def mis_pedidos(request):
    """Historial de pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    
    return render(request, 'usuario/mis_pedidos.html', {
        'pedidos': pedidos
    })


def busqueda_ajax(request):
    """Vista AJAX para búsqueda de productos en tiempo real"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'productos': [], 'count': 0})
    
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) |
        Q(marca__icontains=query) |
        Q(descripcion__icontains=query) |
        Q(categoria__nombre__icontains=query) |
        Q(color__icontains=query) |
        Q(material__icontains=query)
    ).distinct()[:10]  # Limitar a 10 resultados
    
    productos_data = []
    for producto in productos:
        productos_data.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'marca': producto.marca,
            'precio': str(producto.precio),
            'categoria': producto.categoria.nombre,
            'color': producto.color,
            'stock_total': producto.stock_total(),
            'url': f'/producto/{producto.id}/',
        })
    
    return JsonResponse({
        'productos': productos_data,
        'count': len(productos_data),
        'query': query
    })


# ================================
# VISTAS ADMINISTRADOR
# ================================

@user_passes_test(es_admin)
def admin_dashboard(request):
    """Dashboard principal para administradores"""
    from django.db.models import Sum
    from django.utils import timezone
    from datetime import timedelta
    
    # Estadísticas básicas
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()
    total_categorias = Categoria.objects.count()
    
    # Productos con stock bajo (menos de 5 unidades)
    productos_stock_bajo = Producto.objects.filter(
        talla__stock__lt=5
    ).distinct().count()
    
    # Top 3 productos más vendidos (dinámico)
    top_productos = Producto.get_top_vendidos(limit=3)
    
    # Pedidos recientes (últimos 5)
    pedidos_recientes = Pedido.objects.order_by('-fecha_pedido')[:5]
    
    # Ventas del mes actual
    primer_dia_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ventas_mes = Pedido.objects.filter(
        fecha_pedido__gte=primer_dia_mes,
        estado='entregado'
    ).aggregate(Sum('total'))['total__sum'] or 0
    
    # Pedidos completados del mes
    pedidos_completados_mes = Pedido.objects.filter(
        fecha_pedido__gte=primer_dia_mes,
        estado='entregado'
    ).count()
    
    return render(request, 'admin/dashboard.html', {
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'total_categorias': total_categorias,
        'productos_stock_bajo': productos_stock_bajo,
        'top_productos': top_productos,
        'pedidos_recientes': pedidos_recientes,
        'ventas_mes': ventas_mes,
        'pedidos_completados_mes': pedidos_completados_mes,
    })


@user_passes_test(es_admin)
def admin_productos(request):
    """CRUD de productos para administradores"""
    productos = Producto.objects.all().order_by('-fecha_creacion')
    
    return render(request, 'admin/productos_crud.html', {
        'productos': productos
    })


@user_passes_test(es_admin)
def admin_producto_crear(request):
    """Crear nuevo producto con imagen y tallas"""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        talla_formset = TallaFormSet(request.POST, queryset=Talla.objects.none())

        if form.is_valid() and talla_formset.is_valid():
            producto = form.save()

            # Procesar tallas
            for talla_form in talla_formset:
                if talla_form.cleaned_data and not talla_form.cleaned_data.get('DELETE'):
                    talla = talla_form.save(commit=False)
                    talla.producto = producto
                    talla.save()

            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('tienda:admin_productos')
        else:
            if form.errors or talla_formset.errors:
                messages.error(request, 'Error al crear el producto. Revisa los datos.')
    else:
        form = ProductoForm()
        talla_formset = TallaFormSet(queryset=Talla.objects.none())

    return render(request, 'admin/producto_form.html', {
        'form': form,
        'talla_formset': talla_formset,
        'titulo': 'Crear Nuevo Producto',
        'accion': 'Crear'
    })


@user_passes_test(es_admin)
def admin_producto_editar(request, producto_id):
    """Editar producto existente con tallas"""
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        talla_formset = TallaFormSet(request.POST, queryset=producto.talla_set.all())

        if form.is_valid() and talla_formset.is_valid():
            producto = form.save()

            # Procesar tallas
            for talla_form in talla_formset:
                if talla_form.cleaned_data:
                    if talla_form.cleaned_data.get('DELETE'):
                        if talla_form.instance.pk:
                            talla_form.instance.delete()
                    else:
                        talla = talla_form.save(commit=False)
                        talla.producto = producto
                        talla.save()

            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('tienda:admin_productos')
        else:
            if form.errors or talla_formset.errors:
                messages.error(request, 'Error al actualizar el producto. Revisa los datos.')
    else:
        form = ProductoForm(instance=producto)
        talla_formset = TallaFormSet(queryset=producto.talla_set.all())

    # Formulario para imágenes adicionales
    imagen_form = ImagenProductoForm()
    imagenes_adicionales = producto.imagenes.all().order_by('orden', '-fecha_subida')

    return render(request, 'admin/producto_form.html', {
        'form': form,
        'talla_formset': talla_formset,
        'imagen_form': imagen_form,
        'producto': producto,
        'imagenes_adicionales': imagenes_adicionales,
        'titulo': f'Editar: {producto.nombre}',
        'accion': 'Actualizar'
    })


@user_passes_test(es_admin)
def admin_producto_eliminar(request, producto_id):
    """Eliminar producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        return redirect('tienda:admin_productos')
    
    return render(request, 'admin/producto_eliminar.html', {
        'producto': producto
    })


@user_passes_test(es_admin)
def admin_imagen_agregar(request, producto_id):
    """Agregar imagen adicional a producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ImagenProductoForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.producto = producto
            imagen.save()
            messages.success(request, 'Imagen agregada exitosamente.')
        else:
            messages.error(request, 'Error al agregar la imagen.')
    
    return redirect('tienda:admin_producto_editar', producto_id=producto_id)


@user_passes_test(es_admin)
def admin_imagen_eliminar(request, imagen_id):
    """Eliminar imagen adicional"""
    imagen = get_object_or_404(ImagenProducto, id=imagen_id)
    producto_id = imagen.producto.id
    
    if request.method == 'POST':
        imagen.delete()
        messages.success(request, 'Imagen eliminada exitosamente.')
    
    return redirect('tienda:admin_producto_editar', producto_id=producto_id)


@user_passes_test(es_admin)
def admin_categorias(request):
    """CRUD de categorías para administradores"""
    categorias = Categoria.objects.all()
    
    return render(request, 'admin/categorias_crud.html', {
        'categorias': categorias
    })


@user_passes_test(es_admin)
def admin_categoria_crear(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return JsonResponse({
                'success': True,
                'message': f'Categoría "{categoria.nombre}" creada exitosamente.',
                'categoria': {
                    'id': categoria.id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@user_passes_test(es_admin)
def admin_categoria_editar(request, categoria_id):
    """Editar categoría existente"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
            return JsonResponse({
                'success': True,
                'message': f'Categoría "{categoria.nombre}" actualizada exitosamente.',
                'categoria': {
                    'id': categoria.id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    elif request.method == 'GET':
        return JsonResponse({
            'success': True,
            'categoria': {
                'id': categoria.id,
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion
            }
        })
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@user_passes_test(es_admin)
def admin_categoria_eliminar(request, categoria_id):
    """Eliminar categoría"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente.')
        return JsonResponse({
            'success': True,
            'message': f'Categoría "{nombre}" eliminada exitosamente.'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@user_passes_test(es_admin)
def admin_pedidos(request):
    """Gestión de pedidos para administradores"""
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    
    return render(request, 'admin/pedidos.html', {
        'pedidos': pedidos
    })


@user_passes_test(es_admin)
def admin_reportes(request):
    """Reportes y estadísticas para administradores"""
    from django.db.models import Sum, Count
    
    # Actualizar contadores si se solicita
    if request.GET.get('actualizar') == 'ventas':
        productos_actualizados = Producto.actualizar_todas_las_ventas()
        messages.success(request, f'Se actualizaron los contadores de {productos_actualizados} productos.')
    
    # Top productos más vendidos (completo)
    top_productos = Producto.objects.filter(total_vendidos__gt=0).order_by('-total_vendidos')[:10]
    
    # Estadísticas por categoría
    ventas_por_categoria = Categoria.objects.annotate(
        total_vendidos=Sum('producto__total_vendidos')
    ).order_by('-total_vendidos')
    
    productos = Producto.objects.all()
    
    return render(request, 'admin/reportes.html', {
        'productos': productos,
        'top_productos': top_productos,
        'ventas_por_categoria': ventas_por_categoria
    })


@user_passes_test(es_admin)
def actualizar_ventas(request):
    """Vista para actualizar contadores de ventas manualmente"""
    if request.method == 'POST':
        productos_actualizados = Producto.actualizar_todas_las_ventas()
        return JsonResponse({
            'success': True,
            'productos_actualizados': productos_actualizados,
            'message': f'Se actualizaron {productos_actualizados} productos.'
        })

    return JsonResponse({'success': False, 'message': 'Método no permitido'})


# ======================
# SERVICIO WEB JSON API
# ======================

def api_productos_stock(request):
    """
    Servicio web JSON que provee información de productos en stock

    Este servicio es consumido por otros equipos y proporciona:
    - Lista de productos disponibles en stock
    - Información detallada de cada producto
    - Enlaces directos a la visualización de cada producto

    Endpoint: /api/productos-en-stock/
    Método: GET
    Formato de respuesta: JSON
    """
    # Obtener solo productos que tienen stock disponible
    productos_con_stock = Producto.objects.filter(
        tallas__stock__gt=0
    ).distinct().select_related('categoria').prefetch_related('tallas')

    # Construir lista de productos en formato JSON
    productos_data = []
    for producto in productos_con_stock:
        # Obtener URL completa del producto
        producto_url = request.build_absolute_uri(f'/producto/{producto.id}/')

        # Obtener tallas disponibles con stock
        tallas_disponibles = []
        for talla in producto.tallas.filter(stock__gt=0):
            tallas_disponibles.append({
                'talla': talla.talla,
                'stock': talla.stock
            })

        productos_data.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'marca': producto.marca,
            'color': producto.color,
            'material': producto.material,
            'categoria': {
                'id': producto.categoria.id,
                'nombre': producto.categoria.nombre
            },
            'stock_total': producto.stock_total(),
            'tallas_disponibles': tallas_disponibles,
            'total_vendidos': producto.total_vendidos,
            'url': producto_url,
            'imagen_principal': producto.imagen_principal.url if producto.imagen_principal else None
        })

    # Respuesta JSON
    return JsonResponse({
        'success': True,
        'total_productos': len(productos_data),
        'productos': productos_data,
        'message': 'Productos en stock obtenidos exitosamente',
        'proyecto': 'StyleYoung - Tienda Virtual de Ropa',
        'version': '1.0',
        'endpoint': '/api/productos-en-stock/'
    }, json_dumps_params={'ensure_ascii': False, 'indent': 2})


# ======================
# REPORTES CON INVERSIÓN DE DEPENDENCIAS
# ======================

def _generar_reporte_productos(generador_reporte: ReporteInterface, formato: str):
    """
    Función privada que utiliza inversión de dependencias para generar reportes

    Esta función demuestra el principio de Inversión de Dependencias (DIP):
    - Depende de la abstracción (ReporteInterface) y no de implementaciones concretas
    - Permite agregar nuevos formatos sin modificar esta función
    - El cliente decide qué implementación usar

    Args:
        generador_reporte: Instancia de una clase que implementa ReporteInterface
        formato: Nombre del formato (para logging/mensajes)

    Returns:
        HttpResponse con el reporte generado
    """
    # Obtener productos con sus datos
    productos = Producto.objects.select_related('categoria').prefetch_related('tallas').all()

    # Preparar datos para el reporte
    datos_reporte = []
    for producto in productos:
        datos_reporte.append({
            'ID': producto.id,
            'Nombre': producto.nombre,
            'Categoría': producto.categoria.nombre,
            'Marca': producto.marca,
            'Precio': float(producto.precio),
            'Color': producto.color,
            'Material': producto.material,
            'Stock': producto.stock_total(),
            'Vendidos': producto.total_vendidos
        })

    # Columnas del reporte
    columnas = ['ID', 'Nombre', 'Categoría', 'Marca', 'Precio', 'Color', 'Material', 'Stock', 'Vendidos']

    # Generar reporte usando la implementación proporcionada
    return generador_reporte.generar_reporte(
        titulo="Reporte de Productos - StyleYoung",
        datos=datos_reporte,
        columnas=columnas
    )


@user_passes_test(es_admin)
def descargar_reporte_pdf(request):
    """
    Vista para descargar reporte de productos en formato PDF

    Utiliza la implementación ReportePDF gracias a la inversión de dependencias
    """
    generador = ReportePDF()
    return _generar_reporte_productos(generador, 'PDF')


@user_passes_test(es_admin)
def descargar_reporte_excel(request):
    """
    Vista para descargar reporte de productos en formato Excel

    Utiliza la implementación ReporteExcel gracias a la inversión de dependencias
    """
    generador = ReporteExcel()
    return _generar_reporte_productos(generador, 'Excel')


# ======================
# VISTAS API REST
# ======================

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para operaciones CRUD de Productos

    Endpoints disponibles:
    - GET /api/v1/productos/ → Listar todos los productos
    - POST /api/v1/productos/ → Crear nuevo producto
    - GET /api/v1/productos/{id}/ → Obtener detalles de un producto
    - PUT /api/v1/productos/{id}/ → Actualizar un producto
    - DELETE /api/v1/productos/{id}/ → Eliminar un producto
    """
    queryset = Producto.objects.filter(activo=True) if hasattr(Producto, 'activo') else Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
