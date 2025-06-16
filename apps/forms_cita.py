# apps/forms_cita.py

from django import forms
from apps.medical.models.cita import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha', 'hora', 'medico']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'