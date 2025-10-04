from django.db import models

class PlantillaCorreo(models.Model):
    clave = models.CharField(max_length=50, unique=True)  # Ej: CONFIRMACION_CITA
    nombre = models.CharField(max_length=100)             # Ej: "Recordatorio de Cita"
    asunto = models.CharField(max_length=150)
    cuerpo = models.TextField()  # Puedes usar {{nombre}}, {{fecha}}, {{medico}}, {{lugar}}
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.clave})"
