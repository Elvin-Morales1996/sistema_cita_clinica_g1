from django.shortcuts import render
from apps.medical.models.paciente import Paciente
 
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'medical/listar_pacientes.html', {'pacientes': pacientes})
