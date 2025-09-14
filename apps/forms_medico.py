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
            

DIAS = [
    (0,'Lunes'), (1,'Martes'), (2,'Miércoles'),
    (3,'Jueves'), (4,'Viernes'), (5,'Sábado'),
]

class SolicitudAutoCitaForm(forms.Form):
    especialidad = forms.ChoiceField(
        label="Especialidad",
        choices=[],
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_especialidad"})
    )
    medico_id = forms.ModelChoiceField(
        label="Médico (opcional)",
        queryset=Medico.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_medico"})
    )
    # si ya tenías estos campos, déjalos igual:
    dias_preferidos = forms.MultipleChoiceField(
        label="Días preferidos (opcional)",
        choices=[("0","Lun"),("1","Mar"),("2","Mié"),("3","Jue"),("4","Vie"),("5","Sáb"),("6","Dom")],
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
    hora_desde = forms.TimeField(
        label="Desde (opcional)", required=False,
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"})
    )
    hora_hasta = forms.TimeField(
        label="Hasta (opcional)", required=False,
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1) Cargar especialidades distintas
        especialidades = (
            Medico.objects
            .values_list("especialidad", flat=True)
            .distinct()
            .order_by("especialidad")
        )
        self.fields["especialidad"].choices = [("", "— Seleccione —")] + [(e, e) for e in especialidades]

        # 2) Filtrar médicos si ya viene una especialidad seleccionada (POST o GET con datos)
        esp = None
        if self.is_bound:
            esp = self.data.get("especialidad") or self.data.get("especialidad", "")
        else:
            # Si estás pasando initial, también lo soportamos
            esp = self.initial.get("especialidad") if isinstance(self.initial, dict) else None

        if esp:
            self.fields["medico_id"].queryset = Medico.objects.filter(especialidad=esp).order_by("nombre")
        else:
            self.fields["medico_id"].queryset = Medico.objects.none()

    def clean(self):
        cleaned = super().clean()
        esp = cleaned.get("especialidad")
        medico = cleaned.get("medico_id")
        if medico and esp and medico.especialidad != esp:
            self.add_error("medico_id", "El médico elegido no pertenece a la especialidad seleccionada.")
        return cleaned
