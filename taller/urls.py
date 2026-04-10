from django.urls import path
from . import views

app_name = 'taller'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('nuevo/', views.nuevo_servicio, name='nuevo_servicio'),
    
    # Rutas del Inventario
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/nueva/', views.nueva_refaccion, name='nueva_refaccion'),
    path('inventario/editar/<int:refaccion_id>/', views.editar_refaccion, name='editar_refaccion'), 
    
    # Ruta del Detalle
    path('servicio/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
]