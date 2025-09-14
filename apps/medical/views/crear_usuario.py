from django.shortcuts import render, redirect
from apps.forms_usuario import UsuarioForm

def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuario")  # redirige a la lista de usuarios
    else:
        form = UsuarioForm()
    return render(request, "medical/crear_usuario.html", {"form": form})
