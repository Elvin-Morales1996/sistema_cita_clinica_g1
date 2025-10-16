from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    # referenciamos al user model actual
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs"
    )
    action = models.CharField(max_length=255)   # ej. 'login_failed', 'create_patient'
    details = models.TextField(blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = "Log de actividad"
        verbose_name_plural = "Logs de actividad"
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user if self.user else "Anon"
        return f"{self.created_at} - {user_str} - {self.action}"


class AlertRule(models.Model):
    """
    Reglas básicas para alertas: por ejemplo detectar N intentos fallidos en X minutos.
    """
    name = models.CharField(max_length=150)
    action = models.CharField(max_length=150, help_text="Nombre de la acción a vigilar (ej. login_failed)")
    threshold = models.IntegerField(help_text="Número de eventos para disparar alerta")
    window_minutes = models.IntegerField(default=5, help_text="Ventana de tiempo en minutos")
    notify_emails = models.TextField(blank=True, null=True, help_text="Emails separados por comas")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.action})"
    
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    accion = models.CharField(max_length=50, choices=ACTION_CHOICES)
    detalles = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.fecha_hora}"