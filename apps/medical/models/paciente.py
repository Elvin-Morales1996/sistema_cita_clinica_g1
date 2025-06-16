from django.db import models

class Paciente(models.Model):
    identificacion = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ])
    direccion = models.TextField()
    contacto = models.CharField(max_length=20)

    def __str__(self):
     return f"{self.nombre} {self.apellido}"
    
    