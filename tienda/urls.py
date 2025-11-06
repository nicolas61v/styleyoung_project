from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    # URLs para usuarios finales (/)
    path('', views.home, name='home'),
    path('productos/', views.productos_lista, name='productos'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    # APIs AJAX
    path('api/busqueda/', views.busqueda_ajax, name='busqueda_ajax'),
    path('api/actualizar-ventas/', views.actualizar_ventas, name='actualizar_ventas'),

    # Servicio Web JSON para consumo externo
    path('api/productos-en-stock/', views.api_productos_stock, name='api_productos_stock'),
    
    # URLs para administradores (/admin-panel/)
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/productos/', views.admin_productos, name='admin_productos'),
    path('admin-panel/productos/crear/', views.admin_producto_crear, name='admin_producto_crear'),
    path('admin-panel/productos/editar/<int:producto_id>/', views.admin_producto_editar, name='admin_producto_editar'),
    path('admin-panel/productos/eliminar/<int:producto_id>/', views.admin_producto_eliminar, name='admin_producto_eliminar'),
    path('admin-panel/productos/<int:producto_id>/imagen/agregar/', views.admin_imagen_agregar, name='admin_imagen_agregar'),
    path('admin-panel/imagen/eliminar/<int:imagen_id>/', views.admin_imagen_eliminar, name='admin_imagen_eliminar'),
    path('admin-panel/categorias/', views.admin_categorias, name='admin_categorias'),
    path('admin-panel/categorias/crear/', views.admin_categoria_crear, name='admin_categoria_crear'),
    path('admin-panel/categorias/editar/<int:categoria_id>/', views.admin_categoria_editar, name='admin_categoria_editar'),
    path('admin-panel/categorias/eliminar/<int:categoria_id>/', views.admin_categoria_eliminar, name='admin_categoria_eliminar'),
    path('admin-panel/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin-panel/reportes/', views.admin_reportes, name='admin_reportes'),

    # Descargas de reportes (inversión de dependencias)
    path('admin-panel/reportes/descargar-pdf/', views.descargar_reporte_pdf, name='descargar_reporte_pdf'),
    path('admin-panel/reportes/descargar-excel/', views.descargar_reporte_excel, name='descargar_reporte_excel'),
]