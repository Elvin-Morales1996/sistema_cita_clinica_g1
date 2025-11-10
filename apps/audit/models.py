from django.db import models 
from django.conf import settings
from django.utils import timezone
from apps.medical.models import Usuario


class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs"
    )
    action = models.CharField(max_length=255)
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
    name = models.CharField(max_length=150)
    action = models.CharField(max_length=150, help_text="Nombre de la acción a vigilar (ej. login_failed)")
    threshold = models.IntegerField(help_text="Número de eventos para disparar alerta")
    window_minutes = models.IntegerField(default=5, help_text="Ventana de tiempo en minutos")
    notify_emails = models.TextField(blank=True, null=True, help_text="Emails separados por comas")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.action})"


class AuditLog(models.Model):
    ACCIONES = [
        ('user_creation', 'Creación de usuario'),
        ('user_update', 'Actualización de usuario'),
        ('user_deletion', 'Eliminación de usuario'),
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
    ]

    usuario_sistema = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Usuario del sistema clínico"
    )

    usuario_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Usuario del panel admin"
    )

    accion = models.CharField(max_length=50, choices=ACCIONES)
    detalles = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.usuario_sistema:
            return f"{self.usuario_sistema.usuario} - {self.accion}"
        elif self.usuario_admin:
            return f"{self.usuario_admin.username} (admin) - {self.accion}"
        return f"Usuario desconocido - {self.accion}"
