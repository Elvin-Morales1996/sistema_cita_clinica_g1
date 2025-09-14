from django.db import models

ROLES = [
    ('Administrador', 'Administrador'),
    ('Médico', 'Médico'),
    ('Recepcionista', 'Recepcionista'),
    ('Paciente', 'Paciente'),
]

class Usuario(models.Model):
    usuario = models.CharField(max_length=100, unique=True)
    clave = models.CharField(max_length=128)
    rol = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        db_table = "usuario"