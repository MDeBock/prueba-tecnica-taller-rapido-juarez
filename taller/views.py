from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from .models import Servicio, Refaccion, DetalleRefaccion, Mecanico
from .forms import ServicioForm, RefaccionForm, DetalleRefaccionForm

def dashboard(request):
    servicios = Servicio.objects.all().order_by('-creado_el')
    contexto = {'servicios': servicios}
    return render(request, 'taller/dashboard.html', contexto)

def nuevo_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taller:dashboard')
    else:
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

def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    form_detalle = DetalleRefaccionForm()
    error_stock = None
    
    if request.method == 'POST':
        if 'cambiar_estado' in request.POST:
            nuevo_estado = request.POST.get('nuevo_estado')
            if nuevo_estado in dict(Servicio.ESTADOS).keys():
                servicio.estado = nuevo_estado
                servicio.save(update_fields=['estado'])
                return redirect('taller:detalle_servicio', servicio_id=servicio.id)
                
        elif 'agregar_refaccion' in request.POST:
            form_detalle = DetalleRefaccionForm(request.POST)
            if form_detalle.is_valid():
                detalle = form_detalle.save(commit=False)
                refaccion = detalle.refaccion
                cantidad = detalle.cantidad
                
                if cantidad <= refaccion.stock:
                    detalle.servicio = servicio
                    detalle.precio_unitario_neto = refaccion.precio_neto
                    detalle.save() 
                    
                    refaccion.stock -= cantidad
                    refaccion.save(update_fields=['stock'])
                    return redirect('taller:detalle_servicio', servicio_id=servicio.id)
                else:
                    error_stock = f"Stock insuficiente. Solo quedan {refaccion.stock} de {refaccion.nombre}."

    contexto = {
        'servicio': servicio,
        'estados_disponibles': [estado[0] for estado in Servicio.ESTADOS],
        'form_detalle': form_detalle,
        'error_stock': error_stock,
    }
    return render(request, 'taller/detalle_servicio.html', contexto)

def metricas(request):
    # Agrupamos los datos por mecánico para no tener que calcular a mano
    mecanicos = Mecanico.objects.annotate(
        total_servicios=Count('servicios'),
        recaudacion_total=Sum('servicios__gran_total')
    ).order_by('-total_servicios')

    contexto = {
        'mecanicos': mecanicos
    }
    return render(request, 'taller/metricas.html', contexto)