from django.db import models

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField()  # ahora obligatorio
    horario = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre
