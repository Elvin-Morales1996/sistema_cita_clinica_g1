# apps/medical/models/cita.py
from django.db import models
from django.utils import timezone
from apps.medical.models.paciente import Paciente
from apps.medical.models.medico import Medico

class Cita(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("atendida", "Atendida"),
        ("reprogramada", "Reprogramada"),  # 👈 nuevo estado
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    # 🔽 Campos de auditoría/gestión
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    reminder_sent_24 = models.BooleanField(default=False)
    reminder_sent_48 = models.BooleanField(default=False)

    # 🔽 Reprogramaciones
    # Apunta SIEMPRE a la cita raíz (la original)
    cita_origen = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="reprogramaciones",
        on_delete=models.SET_NULL,
        help_text="Si esta cita proviene de una reprogramación, referencia la cita original.",
    )
    # Contador total de reprogramaciones (se mantiene en la cita raíz)
    reprogramaciones_total = models.PositiveIntegerField(default=0)

    def raiz(self):
        return self.cita_origen or self

    def __str__(self):
        return f"{self.paciente} - {self.fecha} {self.hora}"

class CitaReprogramacion(models.Model):
    """
    Historial/auditoría de reprogramaciones.
    """
    cita_origen = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name="historial_reprogramaciones")
    cita_anterior = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name="como_anterior")
    cita_nueva = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name="como_nueva")
    motivo = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reprogramación de {self.cita_anterior_id} a {self.cita_nueva_id} (origen {self.cita_origen_id})"
