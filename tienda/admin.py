from django.contrib import admin
from .models import (
    Categoria, Producto, Talla, CarritoCompras, 
    ItemCarrito, Pedido, ItemPedido
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


class TallaInline(admin.TabularInline):
    model = Talla
    extra = 5


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'categoria', 'color', 'fecha_creacion')
    list_filter = ('categoria', 'marca', 'color', 'material', 'fecha_creacion')
    search_fields = ('nombre', 'marca', 'descripcion')
    inlines = [TallaInline]


@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'talla', 'stock')
    list_filter = ('talla', 'producto__categoria')
    search_fields = ('producto__nombre',)


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    readonly_fields = ('calcular_subtotal',)
    extra = 0


@admin.register(CarritoCompras)
class CarritoComprasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'total', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('usuario__nombre', 'usuario__email')
    inlines = [ItemCarritoInline]


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    readonly_fields = ('calcular_subtotal',)
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'total', 'fecha_pedido')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__nombre', 'usuario__email', 'id')
    inlines = [ItemPedidoInline]
    
    actions = ['marcar_como_procesando', 'marcar_como_enviado', 'marcar_como_entregado']
    
    def marcar_como_procesando(self, request, queryset):
        queryset.update(estado='procesando')
    marcar_como_procesando.short_description = "Marcar como procesando"
    
    def marcar_como_enviado(self, request, queryset):
        queryset.update(estado='enviado')
    marcar_como_enviado.short_description = "Marcar como enviado"
    
    def marcar_como_entregado(self, request, queryset):
        queryset.update(estado='entregado')
    marcar_como_entregado.short_description = "Marcar como entregado"
