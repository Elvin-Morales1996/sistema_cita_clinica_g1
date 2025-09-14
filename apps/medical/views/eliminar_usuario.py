from django.shortcuts import redirect, get_object_or_404
from apps.medical.models import Usuario

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect("usuario")  # 👈 vuelve a la lista de usuarios
