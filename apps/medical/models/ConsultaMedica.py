from django.db import models
from apps.medical.models import Cita, Medico, Paciente

class ConsultaMedica(models.Model):
    #aqui le quite para que permita multiplique consulta aunque solo debe aceptar una
    #cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name="consultas")

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    sintomas = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True, null=True, default="")
    archivos = models.FileField(upload_to="consultas/", blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.paciente} - {self.creado_en.strftime('%Y-%m-%d')}"
