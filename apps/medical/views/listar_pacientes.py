from django.shortcuts import render
from apps.medical.models.paciente import Paciente
from apps.core.services.auth_service import require_role

@require_role(['Administrador', 'Médico', 'Recepcionista'])
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'medical/listar_pacientes.html', {'pacientes': pacientes})
