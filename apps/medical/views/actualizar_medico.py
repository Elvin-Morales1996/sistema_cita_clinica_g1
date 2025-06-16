from django.shortcuts import render, get_object_or_404, redirect
from apps.medical.models.medico import Medico
from apps.forms_medico import PerfilMedicoForm

def actualizar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    
    if request.method == 'POST':
        form = PerfilMedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('listar_medicos')
    else:
        form = PerfilMedicoForm(instance=medico)
        
    return render(request, 'medical/actualizar_medico.html', {'form': form, 'medico': medico})