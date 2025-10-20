# apps/medical/views/actualizar_usuario.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.medical.models.usuario import Usuario
from apps.forms_usuario import UsuarioForm
from apps.core.services.auth_service import require_role
from apps.audit.models import AuditLog
from django.utils import timezone

@require_role(['Administrador'])
def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    rol_anterior = usuario.rol

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_actualizado = form.save()

            # Registrar cambio de rol en auditoría
            if rol_anterior != usuario_actualizado.rol:
                # Obtener el usuario logueado desde la sesión
                usuario_logueado = None
                if request.session.get('user_id'):
                    try:
                        usuario_logueado = Usuario.objects.get(id=request.session['user_id'])
                    except:
                        pass

                AuditLog.objects.create(
                    usuario=usuario_logueado,  # Usuario que realizó el cambio
                    accion='role_change',
                    detalles=f"Cambio de rol del usuario '{usuario_actualizado.usuario}': {rol_anterior} -> {usuario_actualizado.rol}"
                )

            return redirect("usuario")  # vuelve al listado
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, "medical/actualizar_usuario.html", {"form": form, "obj": usuario})
