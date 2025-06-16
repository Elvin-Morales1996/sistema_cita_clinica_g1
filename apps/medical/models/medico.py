from django.db import models


TURNOS = [
    ('turno_dia_1', 'Turno Día 1: 7:00 a.m. – 3:00 p.m. (Lun a Vie; Descanso: Sáb y Dom)'),
    ('turno_dia_2', 'Turno Día 2: 9:00 a.m. – 5:00 p.m. (Mar a Sáb; Descanso: Dom y Lun)'),
    ('turno_noche_1', 'Turno Noche 1: 3:00 p.m. – 11:00 p.m. (Lun a Vie; Descanso: Sáb y Dom)'),
    ('turno_noche_2', 'Turno Noche 2: 11:00 p.m. – 7:00 a.m. (Mié a Dom; Descanso: Lun y Mar)'),
]

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField()  # ahora obligatorio
    horario = models.CharField(max_length=20, choices=TURNOS)

    def __str__(self):
        return self.nombre
