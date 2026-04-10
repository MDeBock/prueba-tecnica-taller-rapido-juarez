from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

# ==========================================
# CONFIGURACIÓN GLOBAL (El panel del Admin)
# ==========================================
class Configuracion(models.Model):
    nombre_taller = models.CharField(max_length=150, default="Taller Juárez")
    # CAMBIO UX: Ahora pide 16, 21, 10.5, etc.
    porcentaje_iva_actual = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('16.00'), help_text="Porcentaje de IVA (Ejemplo: 16 para 16%, 21 para 21%)")

    def save(self, *args, **kwargs):
        self.pk = 1 
        super().save(*args, **kwargs)

    def __str__(self):
        return "Configuración General del Sistema"

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"

def obtener_iva_vigente():
    try:
        config = Configuracion.objects.first()
        # CAMBIO UX: Valor por defecto ahora es 16.00
        return config.porcentaje_iva_actual if config else Decimal('16.00')
    except Exception:
        return Decimal('16.00')

# ==========================================
# MODELOS DEL NEGOCIO
# ==========================================
class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Auto(models.Model):
    placa = models.CharField(max_length=15, unique=True, db_index=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveSmallIntegerField(verbose_name="Año")
    color = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='autos')

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

class Mecanico(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Refaccion(models.Model):
    nombre = models.CharField(max_length=150)
    stock = models.PositiveIntegerField(default=0)
    precio_neto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"

class Servicio(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Terminado', 'Terminado'),
        ('Entregado', 'Entregado'),
    ]

    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='servicios')
    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, related_name='servicios')
    fecha_agenda = models.DateField(db_index=True)
    hora_agenda = models.TimeField()
    km_entrada = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente', db_index=True)
    
    costo_mano_obra_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_refacciones_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    subtotal_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    
    # CAMBIO UX: Guarda el valor entero (ej: 16.00)
    porcentaje_iva_aplicado = models.DecimalField(max_digits=5, decimal_places=2, default=obtener_iva_vigente)
    
    iva_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    gran_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    creado_el = models.DateTimeField(auto_now_add=True)

    def actualizar_totales(self):
        total_refacciones = sum(
            detalle.cantidad * detalle.precio_unitario_neto 
            for detalle in self.refacciones_usadas.all()
        )
        self.costo_refacciones_neto = total_refacciones
        self.subtotal_neto = self.costo_mano_obra_neto + self.costo_refacciones_neto
        
        # CAMBIO UX (MAGIA MATEMÁTICA): Dividimos por 100 aquí mismo
        self.iva_total = self.subtotal_neto * (self.porcentaje_iva_aplicado / Decimal('100'))
        self.gran_total = self.subtotal_neto + self.iva_total
        
        self.save(update_fields=[
            'costo_refacciones_neto', 'subtotal_neto', 
            'porcentaje_iva_aplicado', 'iva_total', 'gran_total'
        ])

    def obtener_botones_estado(self):
        """
        Diccionario centralizado de transiciones permitidas.
        Controla qué botón se dibuja en el HTML según el estado actual.
        """
        transiciones = {
            'Pendiente': [
                {'nuevo_estado': 'En Proceso', 'label': 'INICIAR TRABAJO', 'clase_css': 'btn-primary'}
            ],
            'En Proceso': [
                {'nuevo_estado': 'Terminado', 'label': 'FINALIZAR Y ENVIAR FACTURA', 'clase_css': 'btn-success'}
            ],
            'Terminado': [
                {'nuevo_estado': 'Entregado', 'label': 'REGISTRAR ENTREGA FINAL', 'clase_css': 'btn-dark'}
            ],
            'Entregado': []
        }
        return transiciones.get(self.estado, [])

    def __str__(self):
        return f"Servicio #{self.id} - {self.auto.placa} ({self.estado})"

class DetalleRefaccion(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='refacciones_usadas')
    refaccion = models.ForeignKey(Refaccion, on_delete=models.PROTECT)
    cantidad = models.PositiveSmallIntegerField()
    precio_unitario_neto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al momento")

    def __str__(self):
        return f"{self.cantidad}x {self.refaccion.nombre} (Servicio #{self.servicio.id})"

# ==========================================
# SIGNALS (Disparadores)
# ==========================================
@receiver(post_save, sender=DetalleRefaccion)
@receiver(post_delete, sender=DetalleRefaccion)
def recalcular_totales_servicio(sender, instance, **kwargs):
    instance.servicio.actualizar_totales()

@receiver(post_save, sender=Servicio)
def recalcular_por_mano_obra(sender, instance, created, **kwargs):
    if not kwargs.get('update_fields') or 'gran_total' not in kwargs.get('update_fields', []):
        instance.actualizar_totales()