# cita.py
from django.db import models
from django.utils import timezone
from apps.medical.models.paciente import Paciente  # ajusta la ruta si es distinta
from apps.medical.models.medico import Medico

class Cita(models.Model):
    ESTADOS = [
    ("pendiente", "Pendiente"),
    ("confirmada", "Confirmada"),
    ("cancelada", "Cancelada"),
    ("atendida", "Atendida"),
]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")


    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    reminder_sent_24 = models.BooleanField(default=False)   # 👈 evita NULL
    reminder_sent_48 = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.paciente} - {self.fecha} {self.hora}"