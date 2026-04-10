from django.shortcuts import render, redirect
from .models import Servicio
from .forms import ServicioForm

def dashboard(request):
    servicios = Servicio.objects.all().order_by('-creado_el')
    contexto = {'servicios': servicios}
    return render(request, 'taller/dashboard.html', contexto)

def nuevo_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save() # Guarda en la base de datos y calcula la matemática del IVA
            return redirect('taller:dashboard') # Vuelve a la tabla
    else:
        # Muestra el formulario vacío la primera vez
        form = ServicioForm()
    
    return render(request, 'taller/nuevo_servicio.html', {'form': form})