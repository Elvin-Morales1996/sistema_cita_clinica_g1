from django.shortcuts import render, get_object_or_404, redirect
from apps.medical.models.paciente import Paciente
from apps.pacienteContactoForm import PacienteContactoForm

def editar_contacto_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = PacienteContactoForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')  # Regresa al listado
    else:
        form = PacienteContactoForm(instance=paciente)

    return render(request, 'medical/editar_contacto.html', {
        'form': form,
        'paciente': paciente
    })
