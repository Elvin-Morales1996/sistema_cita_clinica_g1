from django.shortcuts import render
from apps.medical.models.usuario import Usuario
from apps.core.services.auth_service import require_role

@require_role(['Administrador'])
def usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'medical/usuario.html', {'usuarios': usuarios})
