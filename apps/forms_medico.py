from django import forms
from .medical.models import Medico

class PerfilMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'especialidad', 'telefono', 'email', 'horario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'