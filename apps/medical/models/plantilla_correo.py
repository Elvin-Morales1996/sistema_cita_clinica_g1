from django.db import models

class PlantillaCorreo(models.Model):
    clave = models.CharField(max_length=50, unique=True)  # Ej: CONFIRMACION_CITA
    nombre = models.CharField(max_length=100)             # Ej: "Recordatorio de Cita"
    asunto = models.CharField(max_length=150)
    contenido_principal = models.TextField()  # Puedes usar {{nombre}}, {{fecha}}, {{medico}}, {{lugar}}
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

    #Campos nuevos
    despedida = models.TextField(default="Atentamente")
    firma = models.TextField(default="Clínica G1")
    informacion_contacto = models.TextField(default="Contacto: 12345678")
    saludo = models.TextField(default="Estimado/a")


    def __str__(self):
        return f"{self.nombre} ({self.clave})"
