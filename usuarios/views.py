from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Usuario
from .forms import RegistroForm, LoginForm


class RegistroView(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = 'auth/registro.html'
    success_url = reverse_lazy('auth:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuario registrado exitosamente. Ya puedes iniciar sesión.')
        return response


def login_usuario(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Django authenticate espera username, pero usamos email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Verificar si es admin o usuario normal
                if user.is_staff:
                    return redirect('/admin-panel/')
                else:
                    return redirect('/')
            else:
                messages.error(request, 'Credenciales inválidas.')
    
    return render(request, 'auth/login.html', {'form': form})


def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('/')


def login_admin(request):
    """Vista específica para login de administradores"""
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('/admin-panel/')
            else:
                messages.error(request, 'Acceso denegado. Solo administradores pueden acceder.')
    
    return render(request, 'auth/login_admin.html', {'form': form})
