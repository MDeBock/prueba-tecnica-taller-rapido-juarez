from django.shortcuts import render, redirect
from .models import Servicio, Refaccion
from .forms import ServicioForm, RefaccionForm

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

def inventario(request):
    refacciones = Refaccion.objects.all().order_by('nombre')
    return render(request, 'taller/inventario.html', {'refacciones': refacciones})

def nueva_refaccion(request):
    if request.method == 'POST':
        form = RefaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taller:inventario')
    else:
        form = RefaccionForm()
    
    return render(request, 'taller/nueva_refaccion.html', {'form': form})