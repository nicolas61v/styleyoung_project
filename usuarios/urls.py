from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    # URLs para usuarios finales
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    
    # URLs para administradores
    path('admin-auth/login/', views.login_admin, name='admin_login'),
]