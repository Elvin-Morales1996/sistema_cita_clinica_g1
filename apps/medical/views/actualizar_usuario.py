# apps/medical/views/actualizar_usuario.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.medical.models.usuario import Usuario
from apps.forms_usuario import UsuarioForm  

def actualizar_usuario(request, usuario_id): 
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("usuario")  # vuelve al listado
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, "medical/actualizar_usuario.html", {"form": form, "obj": usuario})
