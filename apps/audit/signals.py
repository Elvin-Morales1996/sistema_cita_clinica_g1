from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AuditLog

@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    # Verificamos si el usuario es del admin (modelo User de Django)
    if isinstance(user, User):
        AuditLog.objects.create(
            usuario_admin=user,
            accion='login',
            detalles=f"Inicio de sesión exitoso en el panel de administración"
        )
    else:
        # Usuario del sistema (modelo Usuario)
        AuditLog.objects.create(
            usuario_sistema=user,
            accion='login',
            detalles=f"Inicio de sesión exitoso en el sistema clínico"
        )

@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    if isinstance(user, User):
        AuditLog.objects.create(
            usuario_admin=user,
            accion='logout',
            detalles=f"Cierre de sesión en el panel de administración"
        )
    else:
        AuditLog.objects.create(
            usuario_sistema=user,
            accion='logout',
            detalles=f"Cierre de sesión en el sistema clínico"
        )
