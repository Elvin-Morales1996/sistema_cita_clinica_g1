# views/crear_cita.py
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.forms_cita import CitaForm

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()  # Guardamos la cita
            messages.success(request, '¡La cita se registró con éxito!')

            # Redirige a la misma página para limpiar el formulario
            return redirect('crear_cita')
    else:
        form = CitaForm()

    return render(request, 'medical/Formulariocitas.html', {'form': form})
