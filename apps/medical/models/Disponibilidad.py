from django.db import models
from apps.medical.models.medico import Medico

class DiaNoDisponible(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='dias_no_disponibles')
    fecha = models.DateField()
    motivo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.medico.nombre} no disponible el {self.fecha} ({self.motivo})"
