from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import Servicio, Refaccion, DetalleRefaccion, Mecanico
from .forms import ServicioForm, RefaccionForm, DetalleRefaccionForm
from .utils import generar_pdf_y_enviar_correo

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
        if 'nuevo_estado' in request.POST:
            nuevo_estado = request.POST.get('nuevo_estado')
            estado_anterior = servicio.estado
            
            if nuevo_estado in dict(Servicio.ESTADOS).keys():
                servicio.estado = nuevo_estado
                servicio.save(update_fields=['estado'])
                
                if nuevo_estado == 'Terminado' and estado_anterior != 'Terminado':
                    mail_base = servicio.auto.cliente.email
                    nombre_identificador = servicio.auto.cliente.nombre.replace(' ', '').lower()
                    
                    if mail_base and "@" in mail_base:
                        partes = mail_base.split("@")
                        correo_dinamico = f"{partes[0]}+{nombre_identificador}@{partes[1]}"
                        try:
                            generar_pdf_y_enviar_correo(servicio, correo_dinamico)
                        except Exception as e:
                            print(f"DEBUG Error Email: {e}")
                
                return redirect('taller:detalle_servicio', servicio_id=servicio.id)
                
        elif 'agregar_refaccion' in request.POST:
            form_detalle = DetalleRefaccionForm(request.POST)
            if form_detalle.is_valid():
                detalle = form_detalle.save(commit=False)
                refaccion = detalle.refaccion
                if detalle.cantidad <= refaccion.stock:
                    detalle.servicio = servicio
                    detalle.precio_unitario_neto = refaccion.precio_neto
                    detalle.save() 
                    refaccion.stock -= detalle.cantidad
                    refaccion.save(update_fields=['stock'])
                    return redirect('taller:detalle_servicio', servicio_id=servicio.id)
                else:
                    error_stock = f"Stock insuficiente. Quedan {refaccion.stock} unidades."

    contexto = {
        'servicio': servicio,
        'form_detalle': form_detalle,
        'error_stock': error_stock,
    }
    return render(request, 'taller/detalle_servicio.html', contexto)

def metricas(request):
    ahora = timezone.now()
    
    mecanicos = Mecanico.objects.annotate(
        total_servicios=Count('servicios', filter=Q(servicios__creado_el__month=ahora.month, servicios__creado_el__year=ahora.year)),
        neto_mano_obra=Sum('servicios__costo_mano_obra_neto', filter=Q(servicios__creado_el__month=ahora.month, servicios__creado_el__year=ahora.year)),
        neto_repuestos=Sum('servicios__costo_refacciones_neto', filter=Q(servicios__creado_el__month=ahora.month, servicios__creado_el__year=ahora.year))
    ).order_by('-total_servicios')

    return render(request, 'taller/metricas.html', {
        'mecanicos': mecanicos,
        'mes': ahora.strftime('%B %Y')
    })

def manifest_json(request):
    manifest = """{
        "name": "Taller Juárez",
        "short_name": "Taller",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f8f9fa",
        "theme_color": "#212529"
    }"""
    return HttpResponse(manifest, content_type="application/json")

def service_worker(request):
    sw = """
    self.addEventListener('install', (e) => {
        console.log('[PWA] Instalada');
    });
    self.addEventListener('fetch', (e) => {
    });
    """
    return HttpResponse(sw, content_type="application/javascript")