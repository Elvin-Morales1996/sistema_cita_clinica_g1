from django.db import models

ROLES = [
    ('Administrador', 'Administrador'),
    ('Médico', 'Médico'),
    ('Recepcionista', 'Recepcionista'),
    ('Paciente', 'Paciente'),
]

ESTADOS = [
    ('A', 'Activo'),
    ('I', 'Inactivo'),
]

class Usuario(models.Model):
    usuario = models.CharField(max_length=100, unique=True)
    clave = models.CharField(max_length=128)
    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    class Meta:
        db_table = "usuario"

    @property
    def esta_activo(self):
        return self.estado == 'A'