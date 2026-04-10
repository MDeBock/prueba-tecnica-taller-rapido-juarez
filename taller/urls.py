from django.urls import path
from . import views

app_name = 'taller'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('nuevo/', views.nuevo_servicio, name='nuevo_servicio'),
    
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/nueva/', views.nueva_refaccion, name='nueva_refaccion'),
    path('inventario/editar/<int:refaccion_id>/', views.editar_refaccion, name='editar_refaccion'),
    
    path('servicio/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    
    # Ruta de Métricas
    path('metricas/', views.metricas, name='metricas'),

    # Rutas PWA (Progressive Web App)
    path('manifest.json', views.manifest_json, name='manifest'),
    path('sw.js', views.service_worker, name='sw'),
]