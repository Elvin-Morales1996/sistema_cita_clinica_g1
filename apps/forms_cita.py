# apps/forms_cita.py

from django import forms
from apps.medical.models.cita import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
        }
