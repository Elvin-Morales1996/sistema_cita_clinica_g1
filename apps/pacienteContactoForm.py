from django import forms
from apps.medical.models.paciente import Paciente

class PacienteContactoForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['contacto']  # Solo permitirá editar el contacto
        widgets = {
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nuevo contacto'
            })
        }
