from django.shortcuts import render, redirect, get_object_or_404
from apps.medical.models.cita import Cita

def citas_pendientes(request):
    citas = Cita.objects.filter(estado='pendiente').select_related('paciente', 'medico')
    return render(request, 'medical/citas_pendientes.html', {'citas': citas})

def confirmar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.estado = 'confirmada'
    cita.save()
    return redirect('citas_pendientes')

def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.estado = 'cancelada'
    cita.save()
    return redirect('citas_pendientes')
