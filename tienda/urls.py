from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    # URLs para usuarios finales (/)
    path('', views.home, name='home'),
    path('productos/', views.productos_lista, name='productos'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    # URLs para administradores (/admin-panel/)
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/productos/', views.admin_productos, name='admin_productos'),
    path('admin-panel/categorias/', views.admin_categorias, name='admin_categorias'),
    path('admin-panel/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin-panel/reportes/', views.admin_reportes, name='admin_reportes'),
]