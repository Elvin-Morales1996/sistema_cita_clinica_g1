# views de usuarios
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from apps.medical.models.usuario import Usuario

def eliminar_usuario(request, pk):
    if not request.session.get('is_superadmin'):
        messages.error(request, "Solo el superadministrador puede eliminar usuarios.")
        return redirect('listar_usuarios')

    obj = get_object_or_404(Usuario, pk=pk)
    obj.delete()
    messages.success(request, "Usuario eliminado.")
    return redirect('listar_usuarios')


def toggle_usuario(request, pk):
    # aquí permites admin o superadmin
    if request.method != "POST":
        return redirect('listar_usuarios')

    if request.session.get('rol') != 'Administrador' and not request.session.get('is_superadmin'):
        messages.error(request, "No tienes permisos para activar/desactivar usuarios.")
        return redirect('listar_usuarios')

    obj = get_object_or_404(Usuario, pk=pk)
    obj.estado = 'I' if obj.estado == 'A' else 'A'
    obj.save(update_fields=['estado'])
    messages.success(request, f"Usuario {'activado' if obj.estado=='A' else 'desactivado'}.")
    return redirect(request.POST.get('next') or 'listar_usuarios')
