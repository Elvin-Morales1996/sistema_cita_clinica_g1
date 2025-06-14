from django import forms
from .medical.models import Medico
from .medical.models import Medico, Paciente

class PerfilMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'especialidad', 'telefono', 'email', 'horario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            

class PacienteForm(forms.ModelForm):
     class Meta:
        model = Paciente
        fields = [
            'identificacion',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'sexo',
            'direccion',
            'contacto'
        ]

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'form-control'