from django import forms
from .medical.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['identificacion', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'direccion', 'contacto']
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de identificación'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del paciente'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido del paciente'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Seleccione la fecha de nacimiento'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese la dirección completa'}),
            'contacto': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico'}),
        }
