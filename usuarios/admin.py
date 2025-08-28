from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nombre', 'username', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'nombre', 'username')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('nombre', 'direccion', 'telefono')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal', {'fields': ('email', 'nombre', 'direccion', 'telefono')}),
    )
