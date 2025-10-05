from django import forms
from apps.medical.models.plantilla_correo import PlantillaCorreo

class PlantillaCorreoForm(forms.ModelForm):
    class Meta:
        model = PlantillaCorreo
        fields = ["clave", "nombre", "asunto", "contenido_principal", "despedida"]
        widgets = {
            "contenido_principal": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Escriba el cuerpo del correo con nombre, fecha, medico,lugar"
            }),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "clave": forms.TextInput(attrs={"class": "form-control"}),
            "despedida": forms.TextInput(attrs={"class": "form-control", "placeholder": "Atentamente"}),
            "firma": forms.TextInput(attrs={"class": "form-control", "placeholder": "Firma"}),
            "informacion_contacto": forms.TextInput(attrs={"class": "form-control", "placeholder": "Información de contacto"}),
            "saludo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Estimado/a"}),
    
        }
