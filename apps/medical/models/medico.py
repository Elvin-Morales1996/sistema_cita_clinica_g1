from django.db import models

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    horario = models.CharField(max_length=100, blank=True)  # o usa otro tipo, como JSONField o algo más avanzado

    def __str__(self):
        return self.nombre