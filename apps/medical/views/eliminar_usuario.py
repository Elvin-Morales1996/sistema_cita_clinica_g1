from django.shortcuts import redirect, get_object_or_404
from apps.medical.models import Usuario
from apps.core.services.auth_service import require_role
from apps.audit.models import AuditLog
from django.utils import timezone

@require_role(['Administrador'])
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Registrar eliminación en auditoría antes de eliminar
    # Obtener el usuario logueado desde la sesión
    usuario_logueado = None
    if request.session.get('user_id'):
        try:
            usuario_logueado = Usuario.objects.get(id=request.session['user_id'])
        except Usuario.DoesNotExist:
            usuario_logueado = None

    AuditLog.objects.create(
        usuario=usuario_logueado,  # Usuario que realizó la eliminación
        accion='user_deletion',
        detalles=f"Eliminación del usuario '{usuario.usuario}' con rol '{usuario.rol}'"
    )

    usuario.delete()
    return redirect("usuario") 
