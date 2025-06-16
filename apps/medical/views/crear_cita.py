# views/crear_cita.py
from django.shortcuts import render, redirect
from apps.forms_cita import CitaForm

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # redirige donde desees
    else:
        form = CitaForm()
    return render(request, 'medical/Formulariocitas.html', {'form': form})