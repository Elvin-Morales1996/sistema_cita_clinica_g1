from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.CharField(max_length=1, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
