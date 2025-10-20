from django.shortcuts import render, redirect
from apps.forms_usuario import UsuarioForm
from apps.core.services.auth_service import require_role
from apps.audit.models import AuditLog
from django.utils import timezone

@require_role(['Administrador'])
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario_nuevo = form.save()

            # Registrar creación en auditoría
            # Obtener el usuario logueado desde la sesión
            usuario_logueado = None
            if request.session.get('user_id'):
                try:
                    from apps.medical.models.usuario import Usuario
                    usuario_logueado = Usuario.objects.get(id=request.session['user_id'])
                except:
                    pass

            AuditLog.objects.create(
                usuario=usuario_logueado,  # Usuario que realizó la creación
                accion='user_creation',
                detalles=f"Creación del usuario '{usuario_nuevo.usuario}' con rol '{usuario_nuevo.rol}'"
            )

            return redirect("usuario")  # redirige a la lista de usuarios
    else:
        form = UsuarioForm()
    return render(request, "medical/crear_usuario.html", {"form": form})
