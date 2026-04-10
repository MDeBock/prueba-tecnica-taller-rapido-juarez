from django.shortcuts import render, redirect, get_object_or_404
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

def detalle_servicio(request, servicio_id):
    
    servicio = get_object_or_404(Servicio, id=servicio_id)
    
    
    if request.method == 'POST' and 'cambiar_estado' in request.POST:
        nuevo_estado = request.POST.get('nuevo_estado')
        
        if nuevo_estado in dict(Servicio.ESTADOS).keys():
            servicio.estado = nuevo_estado
            servicio.save(update_fields=['estado'])
            return redirect('taller:detalle_servicio', servicio_id=servicio.id)

    contexto = {
        'servicio': servicio,
        'estados_disponibles': [estado[0] for estado in Servicio.ESTADOS]
    }
    return render(request, 'taller/detalle_servicio.html', contexto)

def editar_refaccion(request, refaccion_id):
    
    refaccion = get_object_or_404(Refaccion, id=refaccion_id)
    
    if request.method == 'POST':
        
        form = RefaccionForm(request.POST, instance=refaccion)
        if form.is_valid():
            form.save()
            return redirect('taller:inventario')
    else:
        
        form = RefaccionForm(instance=refaccion)
    
    return render(request, 'taller/editar_refaccion.html', {'form': form, 'refaccion': refaccion})