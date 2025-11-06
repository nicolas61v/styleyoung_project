"""
Pruebas unitarias para la aplicación tienda
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from tienda.models import Categoria, Producto, Talla, CarritoCompras
from decimal import Decimal

User = get_user_model()


class ProductoTestCase(TestCase):
    """
    Pruebas unitarias para el modelo Producto
    """

    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear categoría de prueba
        self.categoria = Categoria.objects.create(
            nombre="Ropa Casual",
            descripcion="Ropa casual para el día a día"
        )

        # Crear producto de prueba
        self.producto = Producto.objects.create(
            nombre="Camiseta Básica",
            descripcion="Camiseta de algodón 100%",
            precio=Decimal('45000.00'),
            marca="BasicWear",
            color="Blanco",
            material="Algodón",
            categoria=self.categoria
        )

    def test_producto_creacion(self):
        """Prueba 1: Verificar que un producto se crea correctamente"""
        self.assertEqual(self.producto.nombre, "Camiseta Básica")
        self.assertEqual(self.producto.precio, Decimal('45000.00'))
        self.assertEqual(self.producto.categoria, self.categoria)
        self.assertEqual(self.producto.marca, "BasicWear")
        self.assertEqual(self.producto.total_vendidos, 0)

    def test_stock_total_producto(self):
        """Prueba 2: Verificar que el cálculo de stock total funciona correctamente"""
        # Crear tallas con stock para el producto
        Talla.objects.create(producto=self.producto, talla='S', stock=10)
        Talla.objects.create(producto=self.producto, talla='M', stock=15)
        Talla.objects.create(producto=self.producto, talla='L', stock=8)

        # El stock total debe ser la suma de todas las tallas
        stock_total = self.producto.stock_total()
        self.assertEqual(stock_total, 33)  # 10 + 15 + 8 = 33
