from django.shortcuts import render
from apps.medical.models.medico import Medico

def listar_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'medical/listar_medicos.html', {'medicos': medicos})
