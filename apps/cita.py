from django.db import models
from .medical.models import Paciente
from .medical.models import Medico

class Cita(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    id_cita = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Cita {self.id_cita} - {self.paciente.nombre} con {self.medico.nombre} el {self.fecha_cita}"
