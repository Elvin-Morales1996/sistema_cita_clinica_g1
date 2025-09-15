from django.db import models
from .paciente import Paciente

class HistorialClinico(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    antecedentes = models.TextField(blank=True, null=True)
    diagnosticos = models.TextField(blank=True, null=True)
    tratamientos = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial de {self.paciente}"