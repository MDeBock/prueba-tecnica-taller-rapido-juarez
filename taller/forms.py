from django import forms
from .models import Servicio, Refaccion, DetalleRefaccion

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['auto', 'mecanico', 'fecha_agenda', 'hora_agenda', 'km_entrada', 'costo_mano_obra_neto']
        widgets = {
            'fecha_agenda': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_agenda': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'auto': forms.Select(attrs={'class': 'form-select'}),
            'mecanico': forms.Select(attrs={'class': 'form-select'}),
            'km_entrada': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_mano_obra_neto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class RefaccionForm(forms.ModelForm):
    class Meta:
        model = Refaccion
        fields = ['nombre', 'stock', 'precio_neto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Filtro de Aceite'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'precio_neto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

class DetalleRefaccionForm(forms.ModelForm):
    class Meta:
        model = DetalleRefaccion
        fields = ['refaccion', 'cantidad']
        widgets = {
            'refaccion': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }