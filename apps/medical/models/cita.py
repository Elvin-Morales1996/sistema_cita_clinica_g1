from django.db import models

class Cita(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=10)
    fecha = models.DateField()
    hora = models.TimeField()
    medico = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"
