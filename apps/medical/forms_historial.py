from django import forms
from .models import HistorialClinico, Paciente

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['antecedentes', 'diagnosticos', 'tratamientos']
        widgets = {
            'antecedentes': forms.Textarea(attrs={'rows': 4}),
            'diagnosticos': forms.Textarea(attrs={'rows': 4}),
            'tratamientos': forms.Textarea(attrs={'rows': 4}),
        }

class BuscarPacienteForm(forms.Form):
    SEARCH_CHOICES = [
        ('identificacion', 'Identificación'),
        ('nombre_apellido', 'Nombre y Apellido'),
    ]
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, label='Tipo de búsqueda', widget=forms.RadioSelect)
    search = forms.CharField(max_length=100, label='Buscar')