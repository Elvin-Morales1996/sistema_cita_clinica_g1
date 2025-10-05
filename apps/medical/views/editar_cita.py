from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.medical.models.cita import Cita
from apps.forms_cita import CitaForm

def editar_cita(request, cita_id):
    # Obtener la cita o devolver 404
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        # Crear formulario con los datos enviados y la instancia existente
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, '¡La cita se modificó con éxito!')

            # Redirigir al home
            return redirect('home')
    else:
        # Crear formulario con la instancia existente para mostrar los datos actuales
        form = CitaForm(instance=cita)

    # Renderizar plantilla de edición
    return render(request, 'medical/editar_cita.html', {'form': form, 'cita': cita})
