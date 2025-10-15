from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import AuditLog

@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    AuditLog.objects.create(usuario=user, accion='login', detalles='Inicio de sesión exitoso')

@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(usuario=user, accion='logout', detalles='Cierre de sesión')

