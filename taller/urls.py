from django.urls import path
from . import views

app_name = 'taller'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('nuevo/', views.nuevo_servicio, name='nuevo_servicio'),
    
    # Rutas del Inventario
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/nueva/', views.nueva_refaccion, name='nueva_refaccion'),
]