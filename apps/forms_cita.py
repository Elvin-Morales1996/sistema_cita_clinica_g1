# apps/forms_cita.py

from django import forms
from django.forms.widgets import DateInput
from apps.medical.models.cita import Cita
from apps.medical.models.medico import Medico
import datetime

def medico_disponible(medico, fecha, hora):
    dia_semana = fecha.weekday()
    hora_cita = datetime.datetime.strptime(hora, "%H:%M").time()

    turnos = {
        'turno_dia_1': {
            'dias': [0,1,2,3,4],  # Lun-Vie
            'inicio': datetime.time(7, 0),
            'fin': datetime.time(15, 0),
        },
        'turno_dia_2': {
            'dias': [1,2,3,4,5],  # Mar-Sáb
            'inicio': datetime.time(9, 0),
            'fin': datetime.time(17, 0),
        },
        'turno_noche_1': {
            'dias': [0,1,2,3,4],
            'inicio': datetime.time(15, 0),
            'fin': datetime.time(23, 0),
        },
        'turno_noche_2': {
            'dias': [2,3,4,5,6],
            'inicio': datetime.time(23, 0),
            'fin': datetime.time(7, 0),
            'cruza_dia': True,
        }
    }

    turno = turnos.get(medico.horario)
    if not turno or dia_semana not in turno['dias']:
        return False

    if turno.get('cruza_dia'):
        return hora_cita >= turno['inicio'] or hora_cita <= turno['fin']
    else:
        return turno['inicio'] <= hora_cita <= turno['fin']

from apps.medical.models.medico import Medico  # Asegúrate de importar esto

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha', 'hora', 'medico']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Usar calendario para la fecha
        self.fields['fecha'].widget = DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })

        # Horas disponibles (solo ejemplo)
        horas_disponibles = [
            ('09:00', '9:00 AM'),
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('13:00', '1:00 PM'),
            ('14:00', '2:00 PM'),
            ('15:00', '3:00 PM'),
        ]
        self.fields['hora'].widget = forms.Select(choices=horas_disponibles)
        self.fields['hora'].widget.attrs['class'] = 'form-control'

        # Filtrar médicos disponibles si ya hay fecha y hora
        data = self.data or self.initial
        fecha = data.get('fecha')
        hora = data.get('hora')

        if fecha and hora:
            try:
                fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                medicos_disponibles = [
                    m for m in Medico.objects.all()
                    if medico_disponible(m, fecha_obj, hora)
                ]
                self.fields['medico'].queryset = Medico.objects.filter(id__in=[m.id for m in medicos_disponibles])
            except Exception as e:
                pass  
