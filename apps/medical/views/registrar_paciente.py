from django.shortcuts import render, redirect
from apps.forms_medico import PacienteForm

def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_paciente')  # O redirigir a una página de éxito
    else:
        form = PacienteForm()
    
    return render(request, 'medical/registrar_paciente.html', {'form': form})
