from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        # Solo pedimos los datos iniciales. El IVA y los totales se calculan solos.
        fields = ['auto', 'mecanico', 'fecha_agenda', 'hora_agenda', 'km_entrada', 'costo_mano_obra_neto']
        
        # Le inyectamos las clases de Bootstrap para que se adapte a celulares
        widgets = {
            'fecha_agenda': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_agenda': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'auto': forms.Select(attrs={'class': 'form-select'}),
            'mecanico': forms.Select(attrs={'class': 'form-select'}),
            'km_entrada': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_mano_obra_neto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }