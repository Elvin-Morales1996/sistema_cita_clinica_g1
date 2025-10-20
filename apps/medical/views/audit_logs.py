from django.shortcuts import render
from apps.audit.models import AuditLog
from apps.core.services.auth_service import require_role

@require_role(['Administrador'])
def audit_logs_view(request):
    """
    Vista para mostrar el historial de auditoría de cambios de roles y creación de usuarios.
    Solo accesible para administradores.
    """
    # Filtrar solo los logs relacionados con usuarios y roles
    user_related_logs = AuditLog.objects.filter(
        accion__in=['role_change', 'user_creation', 'user_deletion', 'user_update']
    ).order_by('-fecha_hora')

    return render(request, 'medical/audit_logs.html', {
        'audit_logs': user_related_logs
    })