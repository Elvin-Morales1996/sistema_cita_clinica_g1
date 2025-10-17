# apps/forms_reprogramacion.py
from django import forms
from django.db.models import Q
from django.forms.widgets import DateInput
import datetime

from apps.medical.models.cita import Cita
from apps.medical.models.medico import Medico

# Reuso de tu helper:
def medico_disponible(medico, fecha, hora_str):
    import datetime as dt
    dia_semana = fecha.weekday()
    hora_cita = dt.datetime.strptime(hora_str, "%H:%M").time()

    turnos = {
        'turno_dia_1': {'dias': [0,1,2,3,4], 'inicio': dt.time(7,0),  'fin': dt.time(15,0)},
        'turno_dia_2': {'dias': [1,2,3,4,5], 'inicio': dt.time(9,0),  'fin': dt.time(17,0)},
        'turno_noche_1': {'dias': [0,1,2,3,4], 'inicio': dt.time(15,0), 'fin': dt.time(23,0)},
        'turno_noche_2': {'dias': [2,3,4,5,6], 'inicio': dt.time(23,0), 'fin': dt.time(7,0), 'cruza_dia': True},
    }

    turno = turnos.get(getattr(medico, "horario", None))
    if not turno or dia_semana not in turno['dias']:
        return False

    if turno.get('cruza_dia'):
        return hora_cita >= turno['inicio'] or hora_cita <= turno['fin']
    else:
        return turno['inicio'] <= hora_cita <= turno['fin']


class ReprogramarCitaForm(forms.Form):
    fecha = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    hora = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    motivo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        self.cita_actual: Cita = kwargs.pop("cita_actual")
        super().__init__(*args, **kwargs)

        # horas de ejemplo (puedes conectarlo a tu lógica real)
        horas_disponibles = [
            ('09:00', '9:00 AM'), ('10:00', '10:00 AM'), ('11:00', '11:00 AM'),
            ('13:00', '1:00 PM'), ('14:00', '2:00 PM'), ('15:00', '3:00 PM'),
        ]
        self.fields['hora'].choices = horas_disponibles

        # preseleccionar el mismo médico
        self.fields['medico'].initial = self.cita_actual.medico

    def clean(self):
        cleaned = super().clean()
        fecha = cleaned.get("fecha")
        hora = cleaned.get("hora")
        medico = cleaned.get("medico")

        if not (fecha and hora and medico):
            return cleaned

        # 1) disponibilidad por turno
        if not medico_disponible(medico, fecha, hora):
            raise forms.ValidationError("El médico no está disponible en el día/hora seleccionados.")

        # 2) no chocar con otra cita del mismo médico (pendiente/confirmada)
        choque = Cita.objects.filter(
            medico=medico, fecha=fecha, hora=hora
        ).exclude(estado__in=["cancelada", "reprogramada"]).exists()
        if choque:
            raise forms.ValidationError("Ya existe una cita para ese médico en esa fecha/hora.")

        # 3) no permitir retroceder a fecha pasada
        if fecha < datetime.date.today():
            raise forms.ValidationError("No puedes reprogramar a una fecha en el pasado.")

        return cleaned
