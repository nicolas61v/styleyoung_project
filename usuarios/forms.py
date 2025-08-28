from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=100, required=True)
    direccion = forms.CharField(max_length=255, required=True)
    telefono = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'direccion', 'telefono', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS Bootstrap a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Personalizar placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['email'].widget.attrs['placeholder'] = 'correo@ejemplo.com'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Tu nombre completo'
        self.fields['direccion'].widget.attrs['placeholder'] = 'Tu dirección completa'
        self.fields['telefono'].widget.attrs['placeholder'] = '+57 300 123 4567'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirma tu contraseña'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nombre = self.cleaned_data['nombre']
        user.direccion = self.cleaned_data['direccion']
        user.telefono = self.cleaned_data['telefono']
        
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )