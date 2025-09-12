from django.db import models
from django.conf import settings
from decimal import Decimal


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    
    def agregar_producto(self, producto):
        """Agregar producto a la categoría"""
        producto.categoria = self
        producto.save()
    
    def listar_productos(self):
        """Listar productos de la categoría"""
        return self.producto_set.all()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    material = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_principal = models.ImageField(
        upload_to='productos/', 
        blank=True, 
        null=True,
        help_text="Imagen principal del producto"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total_vendidos = models.IntegerField(default=0)
    
    def obtener_detalles(self):
        """Obtener detalles completos del producto"""
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'marca': self.marca,
            'color': self.color,
            'material': self.material,
            'categoria': self.categoria.nombre,
            'tallas_disponibles': self.talla_set.all()
        }
    
    def stock_total(self):
        """Calcular stock total sumando todas las tallas"""
        return sum(talla.stock for talla in self.talla_set.all())
    
    def actualizar_ventas(self):
        """Actualizar el contador de productos vendidos basado en pedidos entregados"""
        from django.db.models import Sum
        total = ItemPedido.objects.filter(
            producto=self,
            pedido__estado='entregado'
        ).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        
        self.total_vendidos = total
        self.save()
        return total
    
    @classmethod
    def get_top_vendidos(cls, limit=3):
        """Obtener los productos más vendidos"""
        return cls.objects.filter(total_vendidos__gt=0).order_by('-total_vendidos')[:limit]
    
    @classmethod
    def actualizar_todas_las_ventas(cls):
        """Actualizar contadores de ventas para todos los productos"""
        productos_actualizados = 0
        for producto in cls.objects.all():
            producto.actualizar_ventas()
            productos_actualizados += 1
        return productos_actualizados
    
    def __str__(self):
        return f"{self.nombre} - {self.marca}"
    
    def obtener_imagen_principal(self):
        """Obtener la imagen principal o la primera imagen disponible"""
        if self.imagen_principal:
            return self.imagen_principal.url
        # Si no tiene imagen principal, buscar en imágenes adicionales
        primera_imagen = self.imagenes.filter(es_principal=True).first()
        if primera_imagen:
            return primera_imagen.imagen.url
        # Si no hay imagen principal marcada, tomar la primera
        primera_imagen = self.imagenes.first()
        if primera_imagen:
            return primera_imagen.imagen.url
        return None
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')
    descripcion = models.CharField(max_length=100, blank=True, help_text="Descripción de la imagen")
    es_principal = models.BooleanField(default=False, help_text="Marcar como imagen principal")
    orden = models.IntegerField(default=0, help_text="Orden de visualización")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Si se marca como principal, desmarcar otras imágenes del mismo producto
        if self.es_principal:
            ImagenProducto.objects.filter(producto=self.producto, es_principal=True).update(es_principal=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre} - {self.descripcion or 'Sin descripción'}"
    
    class Meta:
        verbose_name = "Imagen del Producto"
        verbose_name_plural = "Imágenes del Producto"
        ordering = ['orden', '-fecha_subida']


class Talla(models.Model):
    OPCIONES_TALLA = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    talla = models.CharField(max_length=10, choices=OPCIONES_TALLA)
    stock = models.IntegerField(default=0)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    def verificar_stock(self, cantidad=1):
        """Verificar si hay stock disponible"""
        return self.stock >= cantidad
    
    def reducir_stock(self, cantidad):
        """Reducir stock después de una compra"""
        if self.verificar_stock(cantidad):
            self.stock -= cantidad
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"{self.producto.nombre} - Talla {self.talla} (Stock: {self.stock})"
    
    class Meta:
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"
        unique_together = ['producto', 'talla']


class CarritoCompras(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def agregar_producto(self, producto, talla, cantidad=1):
        """Agregar producto al carrito"""
        item, created = ItemCarrito.objects.get_or_create(
            carrito=self,
            producto=producto,
            talla=talla,
            defaults={'cantidad': cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.save()
        self.calcular_total()
    
    def calcular_total(self):
        """Calcular total del carrito"""
        items = self.itemcarrito_set.all()
        total = sum(item.calcular_subtotal() for item in items)
        self.total = total
        self.save()
        return total
    
    def vaciar_carrito(self):
        """Vaciar todos los items del carrito"""
        self.itemcarrito_set.all().delete()
        self.total = Decimal('0.00')
        self.save()
    
    def __str__(self):
        return f"Carrito de {self.usuario.nombre} - Total: ${self.total}"
    
    class Meta:
        verbose_name = "Carrito de Compras"
        verbose_name_plural = "Carritos de Compras"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(CarritoCompras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    def calcular_subtotal(self):
        """Calcular subtotal del item"""
        return self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Talla {self.talla.talla})"
    
    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ['carrito', 'producto', 'talla']


class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    direccion_entrega = models.CharField(max_length=255)
    
    def procesar_pedido(self):
        """Procesar el pedido"""
        self.estado = 'procesando'
        self.save()
        
        # Crear items del pedido desde el carrito activo
        carrito = CarritoCompras.objects.get(usuario=self.usuario, activo=True)
        for item_carrito in carrito.itemcarrito_set.all():
            ItemPedido.objects.create(
                pedido=self,
                producto=item_carrito.producto,
                talla=item_carrito.talla,
                cantidad=item_carrito.cantidad,
                precio_unitario=item_carrito.producto.precio
            )
            # Reducir stock
            item_carrito.talla.reducir_stock(item_carrito.cantidad)
        
        # Marcar carrito como inactivo
        carrito.activo = False
        carrito.save()
    
    def actualizar_estado(self, nuevo_estado):
        """Actualizar estado del pedido"""
        if nuevo_estado in dict(self.ESTADOS_PEDIDO):
            self.estado = nuevo_estado
            self.save()
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.nombre} - {self.get_estado_display()}"
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def calcular_subtotal(self):
        """Calcular subtotal del item del pedido"""
        return self.precio_unitario * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - Pedido #{self.pedido.id}"
    
    class Meta:
        verbose_name = "Item del Pedido"
        verbose_name_plural = "Items del Pedido"
