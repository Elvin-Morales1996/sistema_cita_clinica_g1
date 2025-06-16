# forms_cita.py
from django import forms
from apps.medical.models.cita import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha', 'hora', 'medico', 'especialidad']

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'medico': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
        }
