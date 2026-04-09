from django.contrib import admin
from .models import Configuracion, Cliente, Auto, Mecanico, Refaccion, Servicio, DetalleRefaccion

# Registro de la configuración global
@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre_taller', 'porcentaje_iva_actual')
    
    # Ocultamos el botón "Añadir" si ya existe una configuración (patrón Singleton)
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(Cliente)
admin.site.register(Auto)
admin.site.register(Mecanico)
admin.site.register(Refaccion)

class DetalleRefaccionInline(admin.TabularInline):
    model = DetalleRefaccion
    extra = 1

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'auto', 'mecanico', 'fecha_agenda', 'estado', 'gran_total')
    list_filter = ('estado', 'mecanico', 'fecha_agenda')
    readonly_fields = ('costo_refacciones_neto', 'subtotal_neto', 'iva_total', 'gran_total')
    inlines = [DetalleRefaccionInline]