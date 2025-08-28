from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']  # username ya no es requerido
    
    def registrarse(self):
        """Método para registrar usuario"""
        self.save()
        
    def __str__(self):
        return f"{self.nombre} ({self.email})"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
