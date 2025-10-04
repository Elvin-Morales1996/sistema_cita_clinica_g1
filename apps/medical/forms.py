from django import forms
from .models import PlantillaCorreo

class PlantillaCorreoForm(forms.ModelForm):
    class Meta:
        model = PlantillaCorreo
        fields = ['clave', 'nombre', 'asunto', 'cuerpo']
        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 6}),
        }
