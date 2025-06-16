# cita.py
from django.db import models
from apps.medical.models.paciente import Paciente  # ajusta la ruta si es distinta
from apps.medical.models.medico import Medico

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.paciente} - {self.fecha} {self.hora}"