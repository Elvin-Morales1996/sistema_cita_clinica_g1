from django import forms
from apps.medical.models.ConsultaMedica import ConsultaMedica


class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = ["sintomas", "diagnostico", "tratamiento", "archivos","observaciones"]
        widgets = {
            "sintomas": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Describa los síntomas del paciente..."
            }),
            "diagnostico": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escriba el diagnóstico clínico..."
            }),
            "tratamiento": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Indique el tratamiento sugerido..."
            }),
            "archivos": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Agregue cualquier observación adicional..."
            }),
        }
