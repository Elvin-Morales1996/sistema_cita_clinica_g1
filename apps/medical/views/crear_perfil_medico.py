from django.shortcuts import render, redirect
from apps.forms_medico import PerfilMedicoForm

def crear_perfil_medico(request):
    if request.method == 'POST':
        form = PerfilMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = PerfilMedicoForm()
    return render(request, 'medical/crear_perfil_medico.html', {'form': form})