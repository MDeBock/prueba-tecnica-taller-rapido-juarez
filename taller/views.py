from django.shortcuts import render
from .models import Servicio

def dashboard(request):
    # Traemos todos los servicios ordenados por los más recientes primero
    servicios = Servicio.objects.all().order_by('-creado_el')
    
    contexto = {
        'servicios': servicios
    }
    return render(request, 'taller/dashboard.html', contexto)