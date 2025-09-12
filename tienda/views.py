from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Producto, Categoria, CarritoCompras, Pedido, Talla, ImagenProducto
from .forms import ProductoForm, CategoriaForm, ImagenProductoForm


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
    
    return render(request, 'usuario/productos.html', {
        'productos': productos,
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
    """Crear nuevo producto con imagen"""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('tienda:admin_productos')
        else:
            messages.error(request, 'Error al crear el producto. Revisa los datos.')
    else:
        form = ProductoForm()
    
    return render(request, 'admin/producto_form.html', {
        'form': form,
        'titulo': 'Crear Nuevo Producto',
        'accion': 'Crear'
    })


@user_passes_test(es_admin)
def admin_producto_editar(request, producto_id):
    """Editar producto existente"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('tienda:admin_productos')
        else:
            messages.error(request, 'Error al actualizar el producto. Revisa los datos.')
    else:
        form = ProductoForm(instance=producto)
    
    # Formulario para imágenes adicionales
    imagen_form = ImagenProductoForm()
    imagenes_adicionales = producto.imagenes.all().order_by('orden', '-fecha_subida')
    
    return render(request, 'admin/producto_form.html', {
        'form': form,
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
