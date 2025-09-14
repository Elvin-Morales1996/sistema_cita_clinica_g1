from django.shortcuts import render
from apps.medical.models.usuario import Usuario

def usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'medical/usuario.html', {'usuarios': usuarios})
